from django.urls import path

from . import views

"""
 Подключение маршрутов "внутри" пакета веб-приложения.
 Маршруты доступа к самим приложениям (apps) представлены в корневом файле urls.py
"""

urlpatterns = [
    path('', views.index, name='index'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.login_user, name='login'),
    path('register/', views.register_user, name='register'),
    # подключаем маршруты для REST API
    path('api/contactrequest/', views.ContactRequestList.as_view()),
    path('api/contactrequest/<int:pk>', views.ContactRequestDetail.as_view()),
]