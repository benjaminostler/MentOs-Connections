from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import Profile

class CreateAccountForm(UserCreationForm):
    first_name = forms.CharField(max_length=15)
    last_name = forms.CharField(max_length=15)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2']
    

class UpdateAccountForm(ModelForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=15)
    last_name = forms.CharField(max_length=15)

    class Meta: 
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

class UpdateProfileForm(ModelForm):
    
    class Meta:
        model = Profile
        fields = ['bio', 'interest', 'status', 'profile_img']
