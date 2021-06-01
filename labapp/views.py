from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.generics import get_object_or_404
#from django.views.decorators.csrf import csrf_protect
from .models import ContactRequest        # импорт ORM-модели данных
from .forms import ContactRequestForm       # импорт модели формы для рендеринга
from .serializers import ContactRequestSerializer       # импорт сериализатора для конвертации модели в json
# Импорт дополнительных модулей для реализации REST API.
# Необходима установка дополнительного пакета: pip3 install djangorestframework
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer       # конвертер ответа (Response) в формат json
from rest_framework.views import APIView
from rest_framework import status

import json

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

def index(request):
    imgs = ['img1.jpg', 'img2.jpg']
    subjs = ["SUBJ_1", "SUBJ_2", "SUBJ_3", "SUBJ_4", "SUBJ_5"]
    # рендеринг (т.е. вставка динамически изменяемых данных) index.html и возвращение готовой страницы
    return render(request, 'labapp/index.html', { 'title': 'Whitesquare', 'pname':'HOME', 'navmenu': navmenu, 'imgs': imgs, 'subjs': subjs })
    #return HttpResponse("This is labapp!")

#@csrf_protect
def contact(request):
    # если используется http-метод GET
    if request.method == 'GET':
        cotact_req_form = ContactRequestForm()
        # рендеринг страницы contact.html
        return render(request, 'labapp/contact.html', { 'title': 'Whitesquare', 'pname':'CONTACT', 'navmenu': navmenu, 'cotact_req_form': cotact_req_form })
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
class ContactRequestList(APIView):
    # Устанавливаем json-тип данных для Response
    renderer_classes = [JSONRenderer]

    # обработка GET-запроса (вывод всех записей)
    def get(self, request):
        # Получаем список всех объектов
        contact_reqs = ContactRequest.objects.all()
        # параметр many=True позволяет сериализовать более одного объекта
        serializer = ContactRequestSerializer(contact_reqs, many=True)
        return Response({ 'contact_requests': serializer.data })

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
        contact_req = self.get_object(pk)
        if not contact_req:
            return Response({'message': 'NOT FOUND'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ContactRequestSerializer(contact_req)
        return Response(serializer.data)

    # HTTP PUT/PATCH
    def put(self, request, pk):
        contact_req = self.get_object(pk)
        if not contact_req:
            return Response({'message': 'NOT FOUND'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ContactRequestSerializer(contact_req, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({ 'message': 'ContactRequest Updated!' }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # HTTP DELETE
    def delete(self, request, pk):
        contact_req = self.get_object(pk)
        if not contact_req:
            return Response({'message': 'NOT FOUND'}, status=status.HTTP_404_NOT_FOUND)
        contact_req.delete()
        return Response({ 'message': 'ContactRequest Deleted!' }, status=status.HTTP_200_OK)

    # Вспомогательный метод, который ищет объект по Primary Key в БД,
    # и если объект не найден возвращает None.
    # Также можно воспользоваться встроенным в Django методом get_object_or_404()
    def get_object(self, pk):
        try:
            return ContactRequest.objects.get(pk=pk)
        except ContactRequest.DoesNotExist:
            return None