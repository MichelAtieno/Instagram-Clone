from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Image, Profile


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text = 'Required')
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    # def save(self, commit=True):
    #     user = super(RegistrationForm, self).save(commit=False)
    #     user.email = cleaned_data['email']
        
    #     if commit:
    #         user.save()

    #     return user

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        exclude = ['comments', 'likes','user_profile']