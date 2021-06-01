from django import forms

"""
Данный файл реализует формы для шаблонов веб-страниц (templates)
"""

# Модель формы на странице contact.html
class ContactRequestForm(forms.Form):
    fname = forms.CharField(label='Имя', max_length=255)
    lname = forms.CharField(label='Фамилия', max_length=255, required=False)
    email = forms.EmailField(label='E-mail', max_length=255)
    SELECT_OPTIONS = (
        ("Сотрудничество", "Сотрудничество"),
        ("Техническая информация", "Техническая информация"),
        ("Ошибка на сайте", "Ошибка на сайте"),
    )
    reqtype = forms.ChoiceField(label='Тип запроса', choices=SELECT_OPTIONS)
    reqtext = forms.CharField(label='Введите текст запроса', widget=forms.Textarea)