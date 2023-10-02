from django.db import models
from passlib.hash import bcrypt
import string
import secrets
from django.core.validators import FileExtensionValidator

class Users(models.Model):
    email = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    name = models.CharField(max_length=200, default='Имя')
    surname = models.CharField(max_length=200, default='Фамилия')
    image = models.ImageField(upload_to='avatars', default='')

    # Получение пароля
    def get_password(self):
        return self.password
    
    # Функция для шифрования пароля
    def hash_password(self, password):
        try:
            # Генерируем хэш пароля
            self.password = bcrypt.hash(password)
            return True
        except:
            return False

    # Функция для проверки совпадения введенного пароля с хэшированным паролем
    def check_password(self, input_password):
        # Проверяем совпадение паролей
        return bcrypt.verify(input_password, self.password)
    
    def generate_password(self):
        # Определите символы, из которых будет генерироваться пароль
        characters = string.ascii_letters + string.digits + string.punctuation
        # Генерируйте случайные символы для пароля заданной длины
        password = ''.join(secrets.choice(characters) for i in range(15))
        self.hash_password(password)
        return password
    

class File(models.Model):
    id_user = models.ForeignKey(Users, on_delete=models.CASCADE, default=1)
    name = models.CharField(max_length=300, default="Название файла")
    file = models.FileField(upload_to='files_users/', 
                            validators=[FileExtensionValidator(allowed_extensions=['mp4', 'mp3', 'png', 'jpg'])])
    name_type = models.CharField(max_length=100, default="TYPE")
    size = models.CharField(max_length=200, default="SIZE")
    create_at = models.DateTimeField(auto_now_add=True)

# Create your models here.
