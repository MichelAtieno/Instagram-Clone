from django.http  import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
def register(request):
    return render(request, 'registration/registration_form.html')




@login_required(login_url='/accounts/login/')
def home(request):
    return render(request, 'home.html')


