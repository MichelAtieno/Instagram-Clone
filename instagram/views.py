from django.http  import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from .email import send_welcome_email
from .forms import RegistrationForm, ImageForm, CommentForm, ProfileForm
from .models import Profile, Image, Comment
from .tokens import account_activation_token


# Create your views here.
def register(request):
    if request.user.is_authenticated():
        return redirect('home')
    else:
        if request.method == 'POST':
            form = RegistrationForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.is_active = False
                user.save()
                current_site = get_current_site(request)
                mail_subject = 'Activate your blog account.'
                message = render_to_string('registration/activate.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                    'token':account_activation_token.make_token(user),
                })
                to_email = form.cleaned_data.get('email')
                email = EmailMessage(
                            mail_subject, message, to=[to_email]
                )
                email.send()
                return HttpResponse('Please confirm your email address to complete the registration')
        else:
            form = RegistrationForm()
            return render(request, 'registration/registration_form.html', {'form':form})

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')


@login_required(login_url='/')
def home(request):
    images = Image.get_images()

    return render(request, 'home.html', {'images':images})


def profile(request, username):
    profile = User.objects.get(username=username)
    # try:
    profile_info = Profile.get_profile(profile.id)
    # # except:
    # profile_info = Profile.filter_by_id(profile.id)
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


        







