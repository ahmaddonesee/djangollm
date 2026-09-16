from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()

class AdminSignUpForm(UserCreationForm):
    email=forms.EmailField(required=True,widget=forms.EmailInput())
    class Meta:
        model=User
        # model=settings.AUTH_USER_MODEL
        fields=('username','email','password1','password2')
        
        
    def save(self, commit=True):
        user = super(AdminSignUpForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['username']
        if commit:
            user.save()
        return user