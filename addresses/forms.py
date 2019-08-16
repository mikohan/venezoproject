from django import forms
from .models import Address
from django.forms import CharField


class AddressForm(forms.ModelForm):
    telephone = CharField(required=True)
    address_line = CharField(required=True)
    city = CharField(required=True)
    class Meta:
        model = Address

        labels = {
            "telephone" : 'Телефон',
            "address_line": "Улица, Дом, Квартира",
            "state": "Область, Регион",
            "city" : "Город, населенный пункт",
            "postal_code" : "Почтовый индекс",
        }

        #fields = '__all__'
        fields = [
            # 'billing_profile',
            # 'address_type',
            'telephone',
            'address_line',
            'state',
            'city',
            'postal_code',
        ]

# class AddressForm(forms.Form):
#     address_line        = forms.CharField(label='Улица Дом Квартира')
#     state               = forms.CharField(label='Регион, область')
#     city                = forms.CharField(label='Населенный пункт')
#     postal_code         = forms.CharField(label='Почтовый индекс')
#
#     class Meta:
#         model = Address