from django.http import HttpResponse, Http404, HttpRequest
from django.views.generic import  DetailView

from .models import  AlegroGoodsSpec, CatSubRusSpec

from django.db.models  import Max
from random import sample
######################################################
from django.http import JsonResponse
from haystack.generic_views import FacetedSearchView as BaseFacetedSearchView
from haystack.query import SearchQuerySet
from .forms import *
from ecommerce.settings import DISCOUNT, IMG_SOURCE_PATH, TMB_SOURCE_PATH
from carts.models import Cart
import os
import http.client as h
from urllib.parse import urlparse
from random import randrange
from django.conf import settings


class ProductDetailView(DetailView):
    model = AlegroGoodsSpec
    template_name = 'shop/detail_product.html'

    def check_image_exist(self, url):
        parse_object = urlparse(url)
        conn = h.HTTPConnection(parse_object.netloc, timeout=1)
        conn.request("HEAD", parse_object.path)
        res = conn.getresponse()
        if res.status == 200:
            return True
        else:
            return False


    def get_context_data(self, **kwargs):
        request = self.request
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        context['product'] = self.model.objects.get(pk=pk)

        # Получаю обьект CatSubRus в переменную
        brad_obj = context['product'].cat_id
        last_cramb = brad_obj.rus_name
        pred_last_crumb = CatSubRusSpec.objects.get(id=brad_obj.parent_id)
        search_string = context['product'].name
        search_string = search_string.split()
        search_string = ' '.join(search_string[:2])
        cart_obj, new_obj = Cart.objects.new_or_get(request)



        context['brad_cat_name'] = pred_last_crumb.rus_name #Это выборки для хлебных крошек
        context['brad_cat_slug'] = pred_last_crumb.slug
        context['brad_subcat_name'] = brad_obj.rus_name
        context['brad_subcat_slug'] = brad_obj.slug
        context['similar'] = SearchQuerySet().autocomplete(content_auto=context['product'].name[:4])[:20]
        context['previous'] = context['similar'][randrange(len(context['similar']))]
        context['next'] = context['similar'][randrange(len(context['similar']))]
        context['cart'] = cart_obj
        context['CDN_SERVER'] = settings.CDN_SERVER
        context['img_list'] = [0, 1, 2, 3, 4, 5, 6, 7]#os.listdir(os.path.join(IMG_SOURCE_PATH, str(pk)))
        #context['tmb_list'] = os.listdir(os.path.join(TMB_SOURCE_PATH, str(pk)))
        return context






###############################################
# Фасетная вьюха для категорий и субкатегорий тоже

class FacetedListCat(BaseFacetedSearchView):

    form_class = FacetedProductListing
    facet_fields = ['cond', 'brand', 'car', 'car_model', 'fuel', 'value', 'category']
    template_name = 'shop/facet_cat.html'
    paginate_by = 12
    context_object_name = 'object_list'



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        request = self.request
        cart_obj, new_obj = Cart.objects.new_or_get(request)
        context['cart'] = cart_obj
        context['CDN_SERVER'] = settings.CDN_SERVER
        context['cats'] = CatSubRusSpec.objects.filter(parent_id=0)

        return context



#Фасетный вывод субкатегорий предпоследний уровень
class FacetedListSubCat(BaseFacetedSearchView):

    form_class = FacetedProductListingSubcat
    facet_fields = ['cond', 'brand', 'car', 'car_model', 'fuel', 'value', 'category']
    template_name = 'shop/facet_cat.html'
    paginate_by = 12
    context_object_name = 'object_list'


    def get_context_data(self,  **kwargs):
        request = self.request
        self.slug = self.kwargs.get('slug')
        context = super().get_context_data(**kwargs)
        url_slug = request.path.split('/')[-2]
        subq = CatSubRusSpec.objects.filter(slug=self.slug).first()
        context['CDN_SERVER'] = settings.CDN_SERVER
        context['cats'] = CatSubRusSpec.objects.filter(parent_id=subq.id)
        context['object_list'] = AlegroGoodsSpec.objects.filter(cat_id=subq.id)
        cart_obj, new_obj = Cart.objects.new_or_get(request)
        context['cart'] = cart_obj

        return context

    def get_form_kwargs(self):
        slug = self.kwargs.get('slug')
        subq = CatSubRusSpec.objects.filter(slug=slug, parent_id=0).first()
        another_sub_ids = list(CatSubRusSpec.objects.filter(parent_id=subq.id).values_list('id', flat=True))
        id_range = list(CatSubRusSpec.objects.filter(parent_id__in=another_sub_ids).values_list('id', flat=True))
        if len(id_range) == 0:
            id_range = another_sub_ids
        rus_name = subq.rus_name
        kwargs = super().get_form_kwargs()
        kwargs.update({'slug': slug, 'slug_id': subq.id, 'rus_name':rus_name, 'id_list':id_range})
        return kwargs


#Фасетный вывод последних категорий
class FacetedListSubSubCat(BaseFacetedSearchView):



    form_class = FacetedProductListingSubcat
    facet_fields = ['cond', 'brand', 'car', 'car_model', 'fuel', 'value', 'category']
    template_name = 'shop/shop_subcategory.html'
    paginate_by = 12
    context_object_name = 'object_list'

    def get_context_data(self, **kwargs):
        self.slug = self.kwargs.get('slug')
        context = super().get_context_data(**kwargs)
        request = self.request
        subq = CatSubRusSpec.objects.filter(slug=self.slug).first()
        context['CDN_SERVER'] = settings.CDN_SERVER
        context['cats'] = CatSubRusSpec.objects.filter(parent_id=subq.id)
        context['object_list'] = AlegroGoodsSpec.objects.filter(cat_id=subq.id)
        context['slug'] = self.slug
        context['rus_name'] = subq.rus_name
        cart_obj, new_obj = Cart.objects.new_or_get(request)
        context['cart'] = cart_obj
        return context

    def get_form_kwargs(self):
        slug = self.kwargs.get('slug')
        subq = CatSubRusSpec.objects.filter(slug=slug).first()
        another_sub_ids = list(
            CatSubRusSpec.objects.filter(parent_id=subq.id).values_list('id', flat=True))
        id_range = list(CatSubRusSpec.objects.filter(parent_id__in=another_sub_ids).filter(id__lt=1000).values_list('id', flat=True))
        if len(id_range) == 0:
            id_range = another_sub_ids
        rus_name = subq.rus_name
        kwargs = super().get_form_kwargs()
        kwargs.update({'slug': slug, 'slug_id': subq.id, 'rus_name': rus_name, 'id_list': id_range})
        return kwargs



class FacetedListSubSubCatLast(BaseFacetedSearchView):



    form_class = FacetedProductListingSubcat
    facet_fields = ['cond', 'brand', 'car', 'car_model', 'fuel', 'value', 'category']
    template_name = 'shop/shop_subcategory_last.html'
    paginate_by = 12
    context_object_name = 'object_list'

    def get_context_data(self, **kwargs):
        self.slug = self.kwargs.get('slug')
        request = self.request
        context = super().get_context_data(**kwargs)
        subq = CatSubRusSpec.objects.filter(slug=self.slug).first()
        #print(subq.parent_id)
        old_q = CatSubRusSpec.objects.filter(id=subq.parent_id).get()
        old_slug, old_name = old_q.slug, old_q.rus_name
        cart_obj, new_obj = Cart.objects.new_or_get(request)
        context['CDN_SERVER'] = settings.CDN_SERVER
        context['cart'] = cart_obj
        context['cats'] = CatSubRusSpec.objects.filter(parent_id=subq.pk)
        context['object_list'] = AlegroGoodsSpec.objects.filter(cat_id=subq.pk)
        context['slug'] = self.slug
        context['rus_name'] = subq.rus_name
        context['old_slug'] = old_slug
        context['old_name'] = old_name
        return context

    def get_form_kwargs(self):
        slug = self.kwargs.get('slug')
        subq = CatSubRusSpec.objects.filter(slug=slug).first()
        id_range = [subq.id,]
        rus_name = subq.rus_name
        kwargs = super().get_form_kwargs()
        kwargs.update({'slug': slug, 'slug_id': subq.id, 'rus_name': rus_name, 'id_list': id_range})
        return kwargs




########## searches features ##################

class FacetedSearchView(BaseFacetedSearchView):

    #form_class = FacetedProductSearchForm
    form_class = FacetedProductListing
    facet_fields = ['cond', 'brand', 'car', 'car_model', 'fuel', 'value', 'category']
    template_name = 'facet/search_res.html'
    paginate_by = 10
    context_object_name = 'object_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        request = self.request
        cart_obj, new_obj = Cart.objects.new_or_get(request)
        context['CDN_SERVER'] = settings.CDN_SERVER
        context['cart'] = cart_obj
        context['cats'] = CatSubRusSpec.objects.filter(parent_id=0)
        return context


def autocomplete(request):
    sqs = SearchQuerySet().autocomplete(
        content_auto=request.GET.get(
            'query',
            ''))[
        :5]
    s = []
    for result in sqs:
        d = {"value": result.name, "data": result.object.id}
        s.append(d)
    output = {'suggestions': s}
    return JsonResponse(output)



