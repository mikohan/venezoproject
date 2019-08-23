from django.db import models
import random, os
from django.db.models.signals import pre_save
from urllib.request import urlopen
from django.urls.base import reverse


from .utils import unique_slug_generator
from .choices import *


def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext

def upload_image_path(instance, filename):
    print (instance)
    print (filename)
    name, ext = get_filename_ext(filename)
    new_filename = random.randint(1, 234982304)
    final_filename = '{}{}'.format(new_filename, ext)
    return f'products/{new_filename}/{final_filename}'

class ProductManager(models.Manager):

    def featured(self):
        return self.get_queryset().filter(featured=True)

    def get_by_id(self, id):
        qs = self.get_quryset().filter(id=id)
        if qs.count() == 1:
            return qs
        else:
            return None


class Product(models.Model):
    title               = models.CharField(max_length=120)
    slug                = models.SlugField(blank=True, unique=True)
    description         = models.TextField()
    price               = models.DecimalField(default=38.99, decimal_places=2, max_digits=20)
    image               = models.ImageField(upload_to=upload_image_path, null=True, blank=True)
    featured            = models.BooleanField(default=False)

    objects = ProductManager()

    def __str__(self):
        return self.title





class SuperCat(models.Model):

    name                = models.CharField(verbose_name='Корневой Раздел', max_length=255, null=True)
    featured            = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Корневые категории'

    def __str__(self):
        return self.name


class CatSubRus(models.Model):
    c_id = models.IntegerField(null=True)
    name = models.CharField(max_length=255, null=True)
    rus_name = models.CharField(max_length=255, null=True)
    parent_id = models.IntegerField(null=True)
    slug = models.CharField(max_length=1000, null=True)
    super_parent = models.ForeignKey(SuperCat, null=True, on_delete=models.CASCADE)

    class Meta:
        db_table = 'cat_sub'
        verbose_name_plural = 'Категории Авто'


    def __str__(self):
        return self.rus_name

    def get_absolute_url(self):
        return reverse('subcat', kwargs={'slug': self.slug})




class AlegroGoods(models.Model):


    name                = models.CharField(max_length=255, null=True)
    allegro_id          = models.CharField(max_length=255, null=True)
    price               = models.IntegerField(null=True)
    price_pol           = models.IntegerField(null=True)
    delivery_price      = models.FloatField(null=True)
    img                 = models.CharField(max_length=1000, null=True)
    cond                = models.CharField(max_length=255, null=True)
    brand               = models.CharField(max_length=255, null=True)
    car                 = models.CharField(max_length=255, null=True)
    car_model           = models.CharField(max_length=100, blank=True, null=True)
    weight              = models.CharField(max_length=255, null=True)
    cat_n               = models.CharField(max_length=255, null=True)
    brand_n             = models.CharField(max_length=255, null=True)
    param               = models.CharField(max_length=1000, null=True)
    description         = models.TextField()
    description_clean   = models.TextField(null=True)
    cat_id              = models.ForeignKey(CatSubRus, related_name='cat_id', on_delete=models.CASCADE, default=1)
    subcat_id           = models.TextField(null=True)
    subsubcat_id        = models.TextField(null=True)
    id_data             = models.CharField(max_length=100, null=True)
    color               = models.CharField(max_length=255, null=True)
    stan                = models.CharField(max_length=255, null=True)
    fuel                = models.CharField(max_length=255, null=True)
    value               = models.CharField(max_length=255, blank=True, null=True)
    trash               = models.CharField(max_length=255, null=True)
    slug                = models.CharField(max_length=255, null=True, unique=True)
    name_pol            = models.CharField(max_length=255, null=True, blank=True)


    class Meta:
        managed = True
        db_table = 'product_allegro'

    def __str__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse('detailed_id', args=[str(self.id)])


class FeaturedProduct(models.Model):

    product_id          = models.ForeignKey(AlegroGoods, on_delete=models.CASCADE, blank=True)
    on_main             = models.IntegerField(choices=MAIN_PAGE_CHOICES, default=1)


    class Meta:
        verbose_name_plural = 'Товары на главной'

    def __str__(self):
        return f'Place: {self.on_main} Product_id: {self.product_id}'


def product_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(product_pre_save_receiver, sender=Product)
