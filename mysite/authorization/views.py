from django.shortcuts import render
from .models import Users

def sign_in(request):
    return render(request, 'authorization/sign in.html')
# Create your views here.
