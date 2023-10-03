from django.shortcuts import render
from django.http import HttpResponse
from .models import Users, File
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import redirect
from django.http import JsonResponse
from social_django.models import UserSocialAuth

import requests

def sign_in(request):
    if request.method == "POST":
        email_get = request.POST.get("email")
        password_get = request.POST.get("password")
        try:
            user = Users.objects.get(email = email_get)
            if user.check_password(password_get):   
                return redirect("mainpage", page_id = user.id)
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


def mainpage(request, page_id):
    user = Users.objects.get(id = int(page_id))
    files = File.objects.filter(id_user = int(page_id))
    avatar = user.image
    
    return render(request, 'authorization/mainpage.html', {"name":user.name, "surname": user.surname, "files": files, "user": user})


def upload_file(request):
    if request.method == 'POST' and request.FILES['file']:
        FK_user = request.POST.get("FK_user")
        user = Users.objects.get(id = int(FK_user))
        file_name = request.POST.get('file_name')
        uploaded_file = request.FILES['file']
        file_size = request.POST.get("file_size")
        file_size = str(int(file_size) // 1024) + " КБ"
        file_type = request.POST.get("file_type")

        # Здесь добавьте код для сохранения данных в базу данных

        file_instance = File(id_user = user, name = file_name, file = uploaded_file, name_type = file_type, size = file_size)
        file_instance.save()

        response_data = {
            'status': 'success',
            'message': 'Файл успешно загружен',
            'file_name': file_name,
            'file_size': file_size,
            'file_type': file_type
        }
        return JsonResponse(response_data)
    else:
        response_data = {
            'status': 'error',
            'message': 'Ошибка при загрузке файла'
        }
        return JsonResponse(response_data, status=400)
    
def changepassword(request):
    if request.method == 'POST':
        FK_user = request.POST.get("FK_user")
        user = Users.objects.get(id = int(FK_user))
        oldpassword = request.POST.get("oldpassword")
        newpassword = request.POST.get("newpassword")
        if user.hash_password(newpassword):
            user.save()
        
        response_data = {
            'status': 'success',
            'message': 'Пароль изменен'
        }
        return JsonResponse(response_data)
    else:
        response_data = {
            'status': 'error',
            'message': 'Ошибка при загрузке пароля'
        }
        return JsonResponse(response_data, status=400)
    
def changeinfo(request):
    if request.method == 'POST':
        FK_user = request.POST.get("FK_user")
        user = Users.objects.get(id = int(FK_user))
        name = request.POST.get("name")
        surname = request.POST.get("surname")
        haveavatar = request.POST.get("haveavatar")

        if haveavatar == "true":
            avatar = request.FILES['avatar']
            user.image = avatar

        if name != "default":
            user.name = name
        
        if surname != "default":
            user.surname = surname

        if haveavatar == "true":
            user.image = avatar

        user.save()

        response_data = {
            'status': 'success',
            'message': 'Данные изменены'
        }
        return JsonResponse(response_data)
    else:
        response_data = {
            'status': 'error',
            'message': 'Ошибка при загрузке данных'
        }
        return JsonResponse(response_data, status=400)



def deletefile(request):
    print("+")
    if request.method == 'POST':
        try:
            FK_user = request.POST.get("FK_user")
            user = Users.objects.get(id = int(FK_user))
            file_id = request.POST.get('idfile')
            print(file_id)
            print(user)
            file_to_delete = File.objects.get(id=file_id)
            file_to_delete.delete()
            return JsonResponse({'message': 'File deleted successfully'})
        except Exception as e:
            return JsonResponse({'error': str(e)})
    return JsonResponse({'error': 'Invalid request method'})

def google_oauth2_callback(request):
    user_social_auth = UserSocialAuth.objects.filter(user=request.user).first()

    user_social_auth and user_social_auth.extra_data
    extra_data = user_social_auth.extra_data
    access_token = extra_data.get('access_token')  # Получаем email из extra_data

    url = 'https://www.googleapis.com/oauth2/v3/userinfo'  # URL для получения информации о пользователе
    headers = {'Authorization': f'Bearer {access_token}'}  # Добавляем токен в заголовки запроса
    response = requests.get(url, headers=headers)  # Отправляем GET запрос к Google API

    email_get = "---"
    if response.status_code == 200:
        user_info = response.json()  # Парсим JSON ответ
        email_get = user_info.get('email')  # Получаем email из ответа
        
    try:
        user = Users.objects.get(email = email_get)
        return redirect("mainpage", page_id = user.id)

    except ObjectDoesNotExist:
        new_user = Users(email = email_get)
        new_user.save()
