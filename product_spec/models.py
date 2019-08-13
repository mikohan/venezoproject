from django.db import models

from django.urls.base import reverse






class CatSubRusSpec(models.Model):
    c_id = models.IntegerField(null=True)
    name = models.CharField(max_length=255, null=True)
    rus_name = models.CharField(max_length=255, null=True)
    parent_id = models.IntegerField(null=True)
    slug = models.CharField(max_length=1000, null=True)

    class Meta:
        db_table = 'cat_sub_spec'
        verbose_name_plural = 'Категории Авто'


    def __str__(self):
        return self.rus_name

    def get_absolute_url(self):
        return reverse('subcat', kwargs={'slug': self.slug})




class AlegroGoodsSpec(models.Model):


    name                = models.CharField(max_length=255, null=True)
    allegro_id          = models.CharField(max_length=255, null=True)
    price               = models.IntegerField(null=True)
    price_pol           = models.IntegerField(null=True)
    delivery_price      = models.FloatField(null=True)
    img                 = models.CharField(max_length=1000)
    cond                = models.CharField(max_length=255)
    brand               = models.CharField(max_length=255)
    car                 = models.CharField(max_length=255)
    car_model           = models.CharField(max_length=100, blank=True)
    weight              = models.CharField(max_length=255, null=True)
    cat_n               = models.CharField(max_length=255, null=True)
    brand_n             = models.CharField(max_length=255, null=True)
    param               = models.CharField(max_length=1000, null=True)
    description         = models.TextField()
    description_clean   = models.TextField(null=True)
    cat_id              = models.ForeignKey(CatSubRusSpec, related_name='cat_id', on_delete=models.CASCADE, default=1)
    subcat_id           = models.CharField(max_length=255, null=True)
    subsubcat_id        = models.CharField(max_length=100, null=True)
    id_data             = models.CharField(max_length=100, null=True)
    color               = models.CharField(max_length=255, null=True)
    stan                = models.CharField(max_length=255, null=True)
    fuel                = models.CharField(max_length=255, null=True)
    value               = models.CharField(max_length=255, null=True)
    #location            = models.CharField(max_length=255, null=True)
    slug                = models.CharField(max_length=255, null=True, unique=True)
    name_pol            = models.CharField(max_length=255, null=True, blank=True)


    class Meta:
        managed = True
        db_table = 'product_allegro_spec'

    def __str__(self):
        return str(self.pk)
