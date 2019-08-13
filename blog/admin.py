from django.contrib import admin

from .models import BlogModel, BlogCategories




class ProductAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'slug']
    class Meta:
        model = BlogModel

admin.site.register(BlogModel)
admin.site.register(BlogCategories)
