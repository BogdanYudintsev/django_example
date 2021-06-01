from django.contrib import admin
from .models import ContactRequest

# Регистрация моделей для доступа через веб-интерфейс админимтратора
admin.site.register(ContactRequest)