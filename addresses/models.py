from django.db import models

from billing.models import BillingProfile

ADDRESS_TYPES = (
    ('billing', 'Адрес плательшика'),
    ('shipping', 'Адрес доставки'),
)

class Address(models.Model):
    billing_profile         = models.ForeignKey(BillingProfile, null=True, on_delete=models.CASCADE)
    address_type            = models.CharField(max_length=120, choices=ADDRESS_TYPES)
    telephone               = models.CharField(max_length=120, null=True, blank=True)
    address_line            = models.CharField(max_length=255, null=True, blank=True)
    city                    = models.CharField(max_length=120, null=True, blank=True)
    country                 = models.CharField(max_length=120, default='Российская Федерация')
    state                   = models.CharField(max_length=120, null=True, blank=True)
    postal_code             = models.CharField(max_length=120, null=True, blank=True)


    def __str__(self):
        return str(self.billing_profile)
