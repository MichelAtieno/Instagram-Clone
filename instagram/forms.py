from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Image, Profile, Comment


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text = 'Required')
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        exclude = ['comments', 'likes','user_profile']

class CommentForm(forms.ModelForm):
    class Meta:
        model =Comment
        exclude = ['image', 'user']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user']
