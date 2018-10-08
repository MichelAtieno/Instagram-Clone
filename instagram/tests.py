from django.test import TestCase
from django.contrib.auth.models import User
from .models import Profile,Image,Comment

# Create your tests here.
class ImageTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='a')
        self.new_image = Image(id =1,image_name='Food', image_caption='Delicious', likes=1, comments='A treat for days',user_profile=self.user)
        

    def test_instance(self):
        self.assertTrue(isinstance(self.new_image,Image))

    def test_save_image(self):
        self.new_image.save()
        images = Image.objects.all()
        self.assertTrue(len(images)>0)

    def test_get_image(self):
        self.new_image.save()
        image = Image.get_image(1)
        self.assertTrue(image==self.new_image)

class ProfileTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(id =1,username='a')
        self.new_profile = Profile(user=self.user, bio='I am awesome')

    def test_instance(self):
        self.assertTrue(isinstance(self.new_profile,Profile))

    def test_get_profile(self):
        self.new_profile.save()
        profile = Profile.get_profile(1)
        self.assertTrue(profile== self.new_profile)

    def test_search_profile(self):
        self.new_profile.save()
        profile = Profile.search_profile('a')
        self.assertTrue(len(profile)==1)

    def test_filter_by_id(self):
        self.new_profile.save()
        profile = Profile.filter_by_id(1)
        self.assertTrue(profile== self.new_profile)

class CommentTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(id =1,username='a')
        self.new_image = Image(image_name='Food', image_caption='Delicious', likes=1, comments='A treat for days',user_profile=self.user)
        self.new_comment = Comment(comment='You are awesome', user=self.user, image=self.new_image)
   
    
    def test_instance(self):
        self.assertTrue(isinstance(self.new_comment,Comment))

    def test_get_comment(self):
        comments = Comment.get_comment(1)
        self.assertTrue(len(comments)==0)
