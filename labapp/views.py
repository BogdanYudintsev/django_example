from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from rest_framework.generics import get_object_or_404
from .models import ContactRequest        # импорт ORM-модели данных
from .forms import ContactRequestForm       # импорт модели формы для рендеринга
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm      # импорт встроенных форм для создания и авторизации пользователя
from django.contrib.auth import authenticate, login     # импорт встроенных методов для проверки учетных данных и авторизации пользователя
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import csrf_protect
from .serializers import ContactRequestSerializer       # импорт сериализатора для конвертации модели в json
# Импорт дополнительных модулей для реализации REST API.
# Необходима установка дополнительного пакета: pip3 install djangorestframework
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer       # конвертер ответа (Response) в формат json
from rest_framework.views import APIView
from rest_framework import status

import json
import datetime

# Структура основного навигационнго меню веб-приложения,
# оформленное в виде массива dict объектов
navmenu = [
    {
        'name': 'HOME',
        'addr': '/'
    },
    {
        'name': 'ABOUT US',
        'addr': '#'
    },
    {
        'name': 'SERVICES',
        'addr': '#'
    },
    {
        'name': 'PROJECTS',
        'addr': '#'
    },
    {
        'name': 'MEMBERS',
        'addr': '#'
    },
    {
        'name': 'CONTACT',
        'addr': '/contact'
    },
]

# Индексная страница
def index(request):
    imgs = ['img1.jpg', 'img2.jpg']
    subjs = ["SUBJ_1", "SUBJ_2", "SUBJ_3", "SUBJ_4", "SUBJ_5"]
    # рендеринг (т.е. вставка динамически изменяемых данных) index.html и возвращение готовой страницы
    return render(request, 'labapp/index.html', { 'title': 'Whitesquare', 'pname':'HOME', 'navmenu': navmenu, 'imgs': imgs, 'subjs': subjs })

# Аутентификация пользователя (Используем встроенную в Django класс формы AuthenticationForm)
def login_user(request):
    # Принимаем POST-запрос с формы на странице login.html
    if request.method == 'POST':
        # Валидируем (проверяем) данные формы
        login_form = AuthenticationForm(data=request.POST)
        # При успешной валидации формы через метод is_valid(), в атрибуте login_form.cleaned_data
        # будут доступны данные, переданные из формы, в виде стандартного объекта dict
        if login_form.is_valid():
            form_data = login_form.cleaned_data
            # Проверяем полученные логин и пароль встроенным в Django методом authenticate
            user = authenticate(username=form_data['username'], password=form_data['password'])
            # если пользователь найден
            if user is not None:
                # если пользователь имеет статус "активный"
                if user.is_active:
                    # используем встроенную в Django функцию login, которая создает сессию пользователя и устанавливает cookie-файл с названием sessionid
                    # данные сессии можно посмотреть, например, с помощью инструкции request.session.items()
                    # dict_items([('_auth_user_id', '1'), ('_auth_user_backend', 'django.contrib.auth.backends.ModelBackend'), ('_auth_user_hash', '9727bbaa4b52a4ce94e01ce732d89e029438fef073f72715c10e46058c104414')])
                    login(request, user)
                    # пример добавления данных в сессию пользователя (сохраняем имя пользователя)
                    request.session['user'] = form_data['username']
                    # пример создания собственного cookie-файла с именем AuthToken,
                    # который содержит некоторые данные из сессии пользователя
                    response = redirect('/')
                    response.set_cookie(
                        'AuthToken',
                        request.session['user'],
                        max_age=None,
                        domain=None,
                        secure=False,
                    )
                    # переадресуем авторизированного пользователя на индексную страницу
                    return response
                else:
                    return HttpResponse('Disabled account')
            else:
                return redirect('/register/')
        else:
            return HttpResponse(str(login_form.errors))
    # Если GET-запрос, то рендерим login.html
    elif request.method == 'GET':
        # рендерим страницу login.html
        login_form = AuthenticationForm()
        return render(request, 'labapp/login.html', { 'title': 'Whitesquare', 'pname':'LOGIN', 'navmenu': navmenu, 'login_form': login_form })

# Регистрация пользователя (Используем встроенную в Django класс формы UserCreationForm)
def register_user(request):
    if request.method == "POST":
        # Валидируем (проверяем) данные формы
        register_form = UserCreationForm(data=request.POST)
        if register_form.is_valid():
            # сохраняем пользователя в БД
            user = register_form.save()
            return redirect('/login/')
        else:
            return HttpResponse(str(register_form.errors))
    elif request.method == 'GET':
        # рендерим страницу login.html
        register_form = UserCreationForm()
        return render(request, 'labapp/register.html', { 'title': 'Whitesquare', 'pname':'LOGIN', 'navmenu': navmenu, 'register_form': register_form })

# Используем встроенный в Django декоратор @login_required
# для разрешения доступа к странице contact.html только авторизированным пользователям
@login_required(login_url='/login/')
def contact(request):
    # если используется http-метод GET
    if request.method == 'GET':
        # используем созданный класс формы из forms.py
        cotact_req_form = ContactRequestForm()
        response = render(request, 'labapp/contact.html', { 'title': 'Whitesquare', 'pname':'CONTACT', 'navmenu': navmenu, 'cotact_req_form': cotact_req_form })
        # рендеринг страницы contact.html
        #return render(request, 'labapp/contact.html', { 'title': 'Whitesquare', 'pname':'CONTACT', 'navmenu': navmenu, 'cotact_req_form': cotact_req_form })
        return response
    # если используется http-метод GET
    elif request.method == 'POST':
        # получаем json-данные из запроса (из формы на странице contact)
        json_data = json.loads(request.body)
        # Формируем объект ContactRequest по данным из json_data
        contactreq = ContactRequest(
            firstname=json_data['firstname'],
            lastname=json_data['lastname'],
            email=json_data['email'],
            reqtype=json_data['reqtype'],
            reqtext=json_data['reqtext'])
        # добавляем данные в БД
        contactreq.save()
        return JsonResponse({ 'message': 'ContactRequest Created!' })

# View-класс для вывода списка всех запросов
class ContactRequestList(LoginRequiredMixin, APIView):
    # адрес переадресации, если данный view-класс требует авторизацию (аргумент LoginRequiredMixin)
    login_url = '/login/'

    # Устанавливаем json-тип данных для Response (в зависимости от заголовка accept в полученном запросе)
    renderer_classes = [JSONRenderer]

    # обработка GET-запроса (вывод всех записей)
    def get(self, request):
        # Получаем список всех объектов
        contactreqs = ContactRequest.objects.all()
        # параметр many=True позволяет сериализовать более одного объекта
        serializer = ContactRequestSerializer(contactreqs, many=True)
        return Response({ 'contactrequests': serializer.data })

    # обработка POST-запроса (добавление новой записи)
    def post(self, request):
        serializer = ContactRequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({ 'message': 'ContactRequest Created!' }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# View-класс реализующий Read, Update, Delete операции над отдельной сущностью (по Primary Key в БД)
class ContactRequestDetail(APIView):
    
    renderer_classes = [JSONRenderer]

    # HTTP GET
    def get(self, request, pk):
        contactreq = self.get_object(pk)
        if not contactreq:
            return Response({'message': 'NOT FOUND'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ContactRequestSerializer(contactreq)
        return Response(serializer.data)

    # HTTP PUT/PATCH
    def put(self, request, pk):
        contactreq = self.get_object(pk)
        if not contactreq:
            return Response({'message': 'NOT FOUND'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ContactRequestSerializer(contactreq, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({ 'message': 'ContactRequest Updated!' }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # HTTP DELETE
    def delete(self, request, pk):
        contactreq = self.get_object(pk)
        if not contactreq:
            return Response({'message': 'NOT FOUND'}, status=status.HTTP_404_NOT_FOUND)
        contactreq.delete()
        return Response({ 'message': 'ContactRequest Deleted!' }, status=status.HTTP_200_OK)

    # Вспомогательный метод, который ищет объект по Primary Key в БД,
    # и если объект не найден возвращает None.
    # Также можно воспользоваться встроенным в Django методом get_object_or_404()
    def get_object(self, pk):
        try:
            return ContactRequest.objects.get(pk=pk)
        except ContactRequest.DoesNotExist:
            return None

