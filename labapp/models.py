from django.db import models
from django.utils import timezone

"""
Файл для описания ORM-моделей пакета
"""

class ContactRequest(models.Model):
    id = models.AutoField(primary_key=True) # Устанавливается по-умолчанию для каждой модели
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255, null=True)
    email = models.CharField(max_length=255, null=True)
    reqtype = models.CharField(max_length=255, null=True)
    reqtext = models.CharField(max_length=255, null=True)
    created_on = models.DateTimeField(auto_now_add=True) # Автоматически записывает текущий таймштамп при первом создании записи
    updated_on = models.DateTimeField(auto_now=True) # Автоматически записывает текущий таймштамп при обновлении
    # Установка названия таблицы
    class Meta:
        db_table = 'contactrequest'
    # Метод определяет вывод модели в строку str()
    def __str__(self):
        return str({'firstname': self.firstname, 'lastname': self.lastname, 'email': self.email, 'reqtype': self.reqtype, 'reqtext': self.reqtext})
