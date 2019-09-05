from django.db import models
import os, random
from django.db.models.signals import pre_save
from .utils import unique_slug_generator
from django.urls.base import reverse

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
    return f'blog/{new_filename}/{final_filename}'


class BlogCategories(models.Model):

    title = models.CharField(max_length=2555)
    slug  = models.SlugField(blank=True, unique=True, max_length=255)

    class Meta:
        verbose_name_plural = 'Категории блога'

    def __str__(self):
        return self.title



class BlogModel(models.Model):
    title               = models.CharField(max_length=120)
    slug                = models.SlugField(blank=True, unique=True, max_length=255)
    description         = models.TextField()
    short_desc          = models.TextField(blank=True)
    image               = models.ImageField(upload_to=upload_image_path, null=True, blank=True)
    category            = models.ForeignKey(BlogCategories,related_name='category', on_delete=models.CASCADE, default=1)
    publish             = models.DateField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Статьи'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('detailed', kwargs={'slug': self.slug})

def blog_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(blog_pre_save_receiver, sender=BlogModel)
pre_save.connect(blog_pre_save_receiver, sender=BlogCategories)





