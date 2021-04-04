from djangoapp.models import Student
from django import forms
from djangoapp.models import UserData
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class StudentForm(forms.ModelForm):
    class Meta:
        model=Student
        fields="__all__"

class TestForm(forms.Form):
    name=forms.CharField(label="Name",max_length=30,widget=forms.TextInput(attrs={
                            'id': 'first_name',
                            'required': True,
                            'placeholder': 'Enter your name',
                            'class':'name'
                        }))    
    email=forms.CharField(label="E-mail",max_length=30,widget=forms.TextInput(attrs={
                            'placeholder':'Enter your e-mail'
                        }))

class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username','first_name', 'last_name', 'email','password1','password2')

class RegForm(forms.ModelForm):
    dob=forms.DateField(label='Date of Birth')
    choices=[('male','Male'),('female','Female')]
    gender = forms.ChoiceField(choices=choices, widget=forms.RadioSelect)
    class Meta:
        model=UserData
        fields=('bio','gender','dob','location')

class CustomerForm(forms.Form):
    cid=forms.IntegerField()
    cfname=forms.CharField(label='Enter first name',max_length=30)
    clname=forms.CharField(label='Enter last name',max_length=30)
    file=forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))