from django.db import models
from django.contrib.auth.models import User
from tinymce.models import HTMLField

# Create your models here.
class Profile(models.Model):
    profile_photo = models.ImageField(upload_to ='prof_pictures/')
    bio = HTMLField()
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, default="")



class Image(models.Model):
    image = models.ImageField(upload_to ='prof_pictures/')
    image_name = models.CharField(max_length = 50)
    image_caption =  models.CharField(max_length = 50)
    profile = models.ForeignKey(Profile)
    likes = models.BooleanField(default=False)
    comments = models.CharField(max_length = 100)
    user_profile = models.ForeignKey(User, on_delete=models.CASCADE, default="")

