from django.http  import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Profile, Image, Comment
from .forms import RegistrationForm, ImageForm, CommentForm, ProfileForm

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            return redirect('accounts/login')
            # return HttpResponse('Confirm email to complete registration')
    else:
        form = RegistrationForm()
        return render(request, 'registration/registration_form.html', {'form':form})


@login_required(login_url='/')
def home(request):
    images = Image.get_images()

    return render(request, 'home.html', {'images':images})


def profile(request, username):
    profile = User.objects.get(username=username)
    try:
        profile_info = Profile.get_profile(profile.id)
    except:
        profile_info = Profile.filter_by_id(profile.id)
    images = Image.get_profile_image(profile.id)
    title = f'@{profile.username}'
    return render(request, 'profile/profile.html', {'title':title, 'profile':profile, 'profile_info':profile_info, 'images':images})  

@login_required(login_url='/accounts/login')
def image(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            upload = form.save(commit=False)
            upload.user_profile = request.user
            upload.save()
            return redirect('profile', username=request.user)
    else:
        form =ImageForm()

    return render(request, 'profile/uploadimage.html', {'form':form})

@login_required(login_url='/accounts/login')
def image_comment(request, image_id):
    image = Image.get_image(image_id)
    comments = Comment.get_comment(image_id)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.image = image
            comment.user = request.user
            comment.save()
            return redirect('image_comment', image_id=image_id)
    else:
        form = CommentForm()

    return render(request, 'comment.html', {'image':image, 'form':form, 'comments':comments})

@login_required(login_url='/accounts/login')
def edit_profile(request):
   
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            edit = form.save(commit=False)
            edit.user = request.user
            edit.save()
            return redirect('profile', username=request.user)
            
    else:
        form = ProfileForm()

    return render(request, 'profile/edit_profile.html', {'form':form, 'profile':profile})

def search_profile(request):
    if 'search' in request.GET and request.GET['search']:
        search_term = request.GET.get('search')
        found_profiles = Profile.search_profile(search_term)
        message = f'{search_term}'

        return render(request, 'search.html',{'message':message, 'profiles':found_profiles})
    else:
        message = 'Enter term to search'
        return render(request, 'search.html', {'message':message})


        







