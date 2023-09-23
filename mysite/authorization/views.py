from django.shortcuts import render
from .models import Users

def sign_in(request):
    return render(request, 'authorization/sign in.html')

def sign_up(request):
    return render(request, 'authorization/sign up.html')

def forgotpassword(request):
    return render(request, 'authorization/forgotpassword.html')

# Create your views here.
