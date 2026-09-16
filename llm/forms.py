from django import forms
from .models import UploadFile,Comment
from django.contrib.auth.models import User


class SignUpForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ["username", "email"]

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")

        if password and password2 and password != password2:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data
    
    
    

# make form for uploadfie model
class UploadFileForm(forms.ModelForm):
    class Meta:
        model=UploadFile
        fields=['name','text','file']
        
# make form for Comment model   
class CommentForm(forms.ModelForm):
    class Meta:
        model=Comment
        fields=['text']