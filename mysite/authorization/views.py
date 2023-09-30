from django.shortcuts import render
from django.http import HttpResponse
from .models import Users
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.conf import settings

def sign_in(request):
    if request.method == "POST":
        email_get = request.POST.get("email")
        password_get = request.POST.get("password")
        try:
            user = Users.objects.get(email = email_get)
            if user.check_password(password_get):
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
            if password_get == repeatpassword_get:    
                new_user = Users(email = email_get)
                if new_user.hash_password(password_get):
                    new_user.save()
                    Complete = '<div class="complete"><div class="textmessage">Вы зарегистрированы</div></div>'
                    ToMain = '<script> setTimeout(function() {window.location.href = "."; }, 3000); </script>'
                    return render(request, 'authorization/sign up.html', {'message': Complete, 'timertomain': ToMain})
                else:
                    Error = '<div class="error"><div class="textmessage">Произошла ошибка!</div></div>'
                    return render(request, 'authorization/sign up.html', {'message': Error})
            else:
                Error = '<div class="error"><div class="textmessage">Пароли не совпадают</div></div>'
                return render(request, 'authorization/sign up.html', {'message': Error})
            

    return render(request, 'authorization/sign up.html')

def forgotpassword(request):
    if request.method == "POST":
        email_get = request.POST.get("email")
        try:
            user = Users.objects.get(email = email_get)

            subject = 'Временный пароль MediaSafe' # Тема
            message = "Уважаемый клиент MediaSafe,\nДля вашей безопасности мы отправляем вам временный пароль для входа в ваш аккаунт." + f"\nВременный пароль: {user.generate_password()}" + "\nПожалуйста, обязательно измените временный пароль на более надежный, следуя этим инструкциям:" + "\n1) Авторизуйтесь на нашем сайте, используя временный пароль и вашу учетную запись" +"\n2) После успешной авторизации, на главной страницу найдите раздел 'Смена пароля'" +"\n3) Введите временный пароль в соответствующее поле, а затем введите ваш новый пароль" +"\n4) Нажмите кнопку 'Сохранить', чтобы завершить процесс смены пароля" +"\n " +"\nЕсли у вас возникли вопросы или сложности при смене пароля, не стесняйтесь обращаться в нашу службу поддержки." +"\n " +"\nСпасибо за то, что выбрали MediaSafe!" +"\n " +"\nС уважением," +"\nКоманда MediaSafe"
            send_mail(subject, message, 'settigs.EMAIL_HOST_USER', [user.email])
            user.save()
            Complete = '<div class="complete"><div class="textmessage">Временный пароль отправлен</div></div>'
            return render(request, 'authorization/forgotpassword.html', {'message': Complete})
        except ObjectDoesNotExist:
            Error = '<div class="error"><div class="textmessage">Пользователь не найден</div></div>'
            return render(request, 'authorization/forgotpassword.html', {'message': Error})
        
    return render(request, 'authorization/forgotpassword.html')


def mainpage(request):
    return render(request, 'authorization/mainpage.html')