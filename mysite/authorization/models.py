from django.db import models
from passlib.hash import bcrypt
import string
import secrets

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
            print(self.password)
            # Генерируем хэш пароля
            self.password = bcrypt.hash(password)
            print(self.password)
            return True
        except:
            return False

    # Функция для проверки совпадения введенного пароля с хэшированным паролем
    def check_password(self, input_password):
        # Проверяем совпадение паролей
        print(self.password)
        return bcrypt.verify(input_password, self.password)
    
    def generate_password(self):
        # Определите символы, из которых будет генерироваться пароль
        characters = string.ascii_letters + string.digits + string.punctuation
        # Генерируйте случайные символы для пароля заданной длины
        password = ''.join(secrets.choice(characters) for i in range(15))
        self.hash_password(password)
        return password
    
# Create your models here.
