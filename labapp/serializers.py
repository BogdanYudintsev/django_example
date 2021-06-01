from rest_framework import serializers
from .models import ContactRequest

"""
В данном модуле реализуются классы валидирующие данные для моделей, представленных в models.py, 
а также сериализующие (преобразующие) данные в необходимый формат (json, xml и т.п.)
"""

class ContactRequestSerializer(serializers.Serializer):
    firstname = serializers.CharField()
    lastname = serializers.CharField(required=False)
    email = serializers.CharField(required=False)
    reqtype = serializers.CharField(required=False)
    reqtext = serializers.CharField()

    # Создает новый экземпляр ContactRequest и возвращает его
    def create(self, validated_data):
        return ContactRequest.objects.create(**validated_data)

    # Обновляет данные в экземпляре ContactRequest и возвращает его
    def update(self, instance, validated_data):
        instance.firstname = validated_data.get('firstname', instance.firstname)
        instance.lastname = validated_data.get('lastname', instance.lastname)
        instance.email = validated_data.get('email', instance.email)
        instance.reqtype = validated_data.get('reqtype', instance.reqtype)
        instance.reqtext = validated_data.get('reqtext', instance.reqtext)
        instance.save()
        return instance