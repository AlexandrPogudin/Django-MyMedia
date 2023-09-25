from django.shortcuts import render
from django.http import HttpResponse
from .models import Users
from django.core.exceptions import ObjectDoesNotExist

def sign_in(request):
    if request.method == "POST":
        email_get = request.POST.get("email")
        password_get = request.POST.get("password")
        try:
            user = Users.objects.get(email = email_get)
            if password_get == user.get_password():
                return HttpResponse(f"Пароль верный")
            else:
                Error = '<div class="error"><div class="textmessage">Пароль не верный</div></div>'
            return render(request, 'authorization/sign in.html', {'message': Error})
        except ObjectDoesNotExist:
            Error = '<div class="error"><div class="textmessage">Пользователь не найден</div></div>'
            return render(request, 'authorization/sign in.html', {'message': Error})
    else:
        return render(request, 'authorization/sign in.html')

def sign_up(request):
    if request.method == "POST":
        email_get = request.POST.get("email")
        password_get = request.POST.get("password")
        repeatpassword_get = request.POST.get("repeatpassword")
        try: 
            user = Users.objects.get(email = email_get)
            Error = '<div class="error"><div class="textmessage">Пользователь уже зарегистрирован</div></div>'
            return render(request, 'authorization/sign up.html', {'message': Error})
        except ObjectDoesNotExist:
            # Регистрация
            Complete = '<div class="complete"><div class="textmessage">Вы зарегистрированы</div></div>'
            ToMain = '<script> setTimeout(function() {window.location.href = "."; }, 3000); </script>'
            return render(request, 'authorization/sign up.html', {'message': Complete, 'timertomain': ToMain})
            

    return render(request, 'authorization/sign up.html')

def forgotpassword(request):
    if request.method == "POST":
        email_get = request.POST.get("email")
        try:
            user = Users.objects.get(email = email_get)
            Complete = '<div class="complete"><div class="textmessage">Временный пароль отправлен</div></div>'
            return render(request, 'authorization/forgotpassword.html', {'message': Complete})
        except ObjectDoesNotExist:
            Error = '<div class="error"><div class="textmessage">Пользователь не найден</div></div>'
            return render(request, 'authorization/forgotpassword.html', {'message': Error})
        
    return render(request, 'authorization/forgotpassword.html')
