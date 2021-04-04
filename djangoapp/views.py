from django.shortcuts import render,redirect
from django.http import HttpResponse
from djangoapp.models import Student
from djangoapp.form import StudentForm,TestForm,UserForm,RegForm,CustomerForm
from reportlab.pdfgen import canvas
from django.core.mail import send_mail
from djangop import settings
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from djangoapp.functions import handle_uploaded_file
import csv

# Create your views here.

def index(request):
    return HttpResponse("Welcome to Django!")

def display(request):
    return render(request,"test.html")

def test(request):
    return render(request,"test2.html")

def showstudents(request):
    students=Student.objects.all()
    return render(request,"students.html",{'students':students})

def createstudent(request): 
     if request.method=="POST": 
          form=StudentForm(request.POST) 
          if form.is_valid(): 
               form.save() 
               return redirect("/showstudents/") 
     else: 
          form=StudentForm() 
          return render(request,"createstudent.html",{'form':form}) 

def delete(request,id): 
     student=Student.objects.get(id=id) 
     student.delete() 
     return redirect("/showstudents/") 

def edit(request,id): 
     student=Student.objects.get(id=id) 
     if request.method=="POST":           
          form=StudentForm(request.POST,instance=student) 
          if form.is_valid(): 
               form.save() 
               return redirect("/showstudents/") 
     else: 
          form=StudentForm() 
     return render(request,"editstudent.html",{'form':form,'student':student}) 

def setsession(request):
     if request.method=="POST":
          form=TestForm(request.POST)
          if form.is_valid():
               name=request.POST['name']
               email=request.POST['email']
               request.session["name"]=name #stores name in session
               request.session["email"]=email #stores email in session
               return redirect('/getsession')
     else:
          form=TestForm()
     return render(request,'sess.html',{'form':form})

def getsession(request):
     name=request.session["name"]   #fetches session value
     email=request.session["email"] #fetches session value
     return render(request,'result.html',{'name':name,'email':email})

def setcookie(request):
     response=HttpResponse("Cookie set")
     response.set_cookie("mycookie","abcd")
     #mycookie is cookie name,abcd is cookie value
     return response

def getcookie(request):
     cookievalue=request.COOKIES["mycookie"]#fetches cookie value
     return HttpResponse("Cookie value is "+cookievalue)

def getpdf(request):
     response=HttpResponse(content_type='application/pdf')
     response['Content-Disposition']='attachment;filename="sample.pdf"'
     c=canvas.Canvas(response)
     c.setFont("Times-Roman",42)
     c.drawString(100,700,"Hello user!")
     c.showPage()
     c.save()
     return response

def getcsv(request):
     response=HttpResponse(content_type='text/csv')
     response['Content-Disposition']='attachment;filename="student.csv"'
     writer=csv.writer(response)
     writer.writerow(['Id','Name','Marks'])
     writer.writerow(['100','Kundan','90'])
     writer.writerow(['101','Rehan','92'])
     return response

def sendmail(request):
     subject = "Greetings"
     msg = "Congratulations for your success"
     to = "kundankumardec16@gmail.com"
     res = send_mail(subject, msg, settings.EMAIL_HOST_USER, [to])
     if(res == 1):
          msg = "Mail sent successfully"
     else:
          msg = "Mail could not be sent"
     return HttpResponse(msg)

def customreg(request):
     if request.method=="POST":
          user=UserForm(request.POST)
          form=RegForm(request.POST)
          if user.is_valid() and form.is_valid():
               profile = form.save(commit=False)
               profile.user = request.user
               user.save()
               profile.save()
               return redirect("/login/")
     else:
          user=UserForm()
          form=RegForm()
     return render(request,"registration/customreg.html",{'form':form,'user':user})

def check(request):
     username=request.POST['username']
     password=request.POST['password']
     user=authenticate(request,username=username,password=password)
     if user is not None:
          login(request,user)#logs in the user
          return redirect("/home")
     else:
          return redirect("/login")

@login_required
def home(request):
     username=request.user.username
     return render(request,"home.html",{'username':username})

def logoutview(request):
     logout(request)#logsout the current user
     return redirect("/login")

def uploader(request):
     if request.method=="POST":
          form=CustomerForm(request.POST,request.FILES)
          if form.is_valid():
               for f in request.FILES.getlist('file'):
                    handle_uploaded_file(f)
               #return render(request,'customer.html',{'form':form,'fi':request.FILES['file']})
               return HttpResponse('file uploaded successfully')
     else:
          c=CustomerForm()
          return render(request,'customer.html',{'form':c})
