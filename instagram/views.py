from django.http  import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Profile, Image
from .forms import RegistrationForm 

# Create your views here.
def register(request):
        if request.method == 'POST':
            form = RegistrationForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.is_active = False
                user.save()
                current_site = get_current_site(request)
                return HttpResponse('Confirm email to complete registration')
        else:
            form = RegistrationForm()
            return render(request, 'registration/registration_form.html', {'form':form})


    




@login_required(login_url='/accounts/login/')
def home(request):
    return render(request, 'home.html')


