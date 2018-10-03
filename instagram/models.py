from django.db import models

# Create your models here.
class Profile(models.Model):
    profile_photo = models.ImageField(upload_to ='prof_pictures/')
    bio = models.CharField(max_length = 100)



class Image(models.Model):
    image = models.ImageField(upload_to ='prof_pictures/')
    image_name = models.CharField(max_length = 50)
    image_caption =  models.CharField(max_length = 50)
    profile = models.ForeignKey(Profile)
    likes = models.BooleanField(default=False)
    comments = models.CharField(max_length = 100)

