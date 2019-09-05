from django.contrib.sitemaps import Sitemap
from product.models import AlegroGoods, CatSubRus
from blog.models import BlogModel

class BlogsSitemaps(Sitemap):

    def items(self):
        return BlogModel.objects.all()

class ProductSitemaps(Sitemap):

    def items(self):
        return AlegroGoods.objects.all()



class CategoriesSitemaps(Sitemap):

    def items(self):

        return CatSubRus.objects.all()
    

