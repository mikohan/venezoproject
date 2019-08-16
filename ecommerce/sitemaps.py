from django.contrib.sitemaps import Sitemap
from product.models import AlegroGoods, CatSubRus



class ProductSitemaps(Sitemap):

    def items(self):
        return AlegroGoods.objects.all()



class CategoriesSitemaps(Sitemap):

    def items(self):
        return CatSubRus.objects.all()
    
