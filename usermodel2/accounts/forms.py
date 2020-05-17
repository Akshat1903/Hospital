from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
from .models import DoctorProfile,Patient

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta():
        model = User
        fields = ('username','email','password')

class DoctorProfileForm(forms.ModelForm):
    class Meta():
        model = DoctorProfile
        fields = ('speciality','phonenumber','image')

class UserUpdateForm(UserChangeForm):

     class Meta:
         model = User
         fields = ('email','first_name','last_name','password')

class DoctorProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = DoctorProfile
        fields = ('speciality','phonenumber','image')

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        exclude = ['doctor',]
