from django.db import models
from carts.models import Cart
from .utils import unique_order_id_generator
from django.db.models.signals import pre_save, post_save
from math import fsum
from billing.models import BillingProfile
from addresses.models import Address

ORDER_STATUS_CHOICES = (
    ('created', 'Created'),
    ('paid', 'Paid'),
    ('shipped', 'Shipped'),
    ('delivered', 'Delivered')

)


class OrderManager(models.Manager):
    def new_or_get(self, billing_profile, cart_obj):
        qs = self.model.objects.filter(billing_profile=billing_profile, cart=cart_obj, active=True, status='created')
        if qs.count() == 1:
            created = False
            obj = qs.first()
        else:
            obj = self.model.objects.create(billing_profile=billing_profile, cart=cart_obj)
            created = True
        return obj, created




class Order(models.Model):
    billing_profile             = models.ForeignKey(BillingProfile, null=True, on_delete=models.SET_NULL)
    order_id                    = models.CharField(max_length=255, blank=True)
    shipping_address            = models.ForeignKey(Address, related_name='shipping_address', null=True, blank=True, on_delete=models.CASCADE)
    billing_address             = models.ForeignKey(Address, related_name='billing_address', null=True, blank=True, on_delete=models.CASCADE)
    cart                        = models.ForeignKey(Cart, null=True, on_delete=models.SET_NULL)
    status                      = models.CharField(max_length=255, default='created', choices=ORDER_STATUS_CHOICES)
    shipping_total              = models.DecimalField(default=0, max_digits=20, decimal_places=0)
    total                       = models.DecimalField(default=0, max_digits=20, decimal_places=0)
    active                      = models.BooleanField(default=True)


    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return self.order_id

    objects = OrderManager()

    def update_total(self):
        cart_total = self.cart.total
        shipping_total = self.shipping_total
        new_total = format(fsum([cart_total, shipping_total]), '.0f')
        self.total = new_total
        self.save()
        return new_total

    def check_done(self):
        billing_profile = self.billing_profile
        shipping_address = self.shipping_address
        total = self.total
        if billing_profile and shipping_address and total > 0:
            return True
        return False

    def mark_paid(self):
        if self.check_done():
            self.status = "paid"
            self.save()
        return self.status



def pre_save_create_order_id(sender, instance, *args, **kwargs):
    if not instance.order_id:
        instance.order_id = unique_order_id_generator(instance)
    qs = Order.objects.filter(cart=instance.cart).exclude(billing_profile=instance.billing_profile)
    print(instance.billing_profile, instance.cart)
    if qs.exists():
        qs.update(active=False)

pre_save.connect(pre_save_create_order_id, sender=Order)

def post_save_cart_total(sender, instance, created, *args, **kwargs):
    if not created:
        cart_obj = instance
        cart_total = cart_obj.total
        cart_id = cart_obj.id
        qs = Order.objects.filter(cart__id=cart_id)
        if qs.count() == 1:
            order_obj = qs.first()
            order_obj.update_total()

post_save.connect(post_save_cart_total, sender=Cart)


def post_save_order(sender, instance, created, *args, **kwargs):
    if created:
        instance.update_total()

post_save.connect(post_save_order, sender=Order)