from haystack.forms import FacetedSearchForm
from ecommerce.settings import MIN_PRICE
from .models import CatSubRusSpec
from django.http import HttpResponse, Http404, HttpRequest


class FacetedProductSearchForm(FacetedSearchForm):

    def __init__(self, *args, **kwargs):
        data = dict(kwargs.get("data", []))
        self.conds = data.get('cond', [])
        self.brands = data.get('brand', [])
        self.cars = data.get('car', [])
        self.car_models = data.get('car_models', [])
        self.fuels = data.get('fuel', [])
        self.values = data.get('value', [])
        self.prices = data.get('prices', []),
        self.categories = data.get('category', [])
        super().__init__(*args, **kwargs)


    def search(self):
        if not self.cleaned_data.get("q") or self.cleaned_data.get("q") == '' or self.cleaned_data.get("q") is None:
            #return self.no_query_found()
            sqs = self.searchqueryset.filter(price__gt=MIN_PRICE)
            pass
        else:
            sqs = super().search()

        if self.car_models:
            query = None
            for car_model in self.car_models:
                if query:
                    query += u' AND '
                else:
                    query = u''
                query += u'"%s"' % sqs.query.clean(car_model)
            sqs = sqs.narrow(u'car_model_exact:%s' % query)


        if self.conds:
            query = None
            for cond in self.conds:
                if query:
                    query += u' AND '
                else:
                    query = u''
                query += u'"%s"' % sqs.query.clean(cond)
            sqs = sqs.narrow(u'cond_exact:%s' % query)

        if self.brands:
            query = None
            for brand in self.brands:
                if query:
                    query += u' AND '
                else:
                    query = u''
                query += u'"%s"' % sqs.query.clean(brand)
            sqs = sqs.narrow(u'brand_exact:%s' % query)

        if self.cars:
            query = None
            for car in self.cars:
                if query:
                    query += u' AND '
                else:
                    query = u''
                query += u'"%s"' % sqs.query.clean(car)
            sqs = sqs.narrow(u'car_exact:%s' % query)

        if self.fuels:
            query = None
            for fuel in self.fuels:
                if query:
                    query += u' AND '
                else:
                    query = u''
                query += u'"%s"' % sqs.query.clean(fuel)
            sqs = sqs.narrow(u'fuel_exact:%s' % query)

        if self.values:
            query = None
            for value in self.values:
                if query:
                    query += u' AND '
                else:
                    query = u''
                query += u'"%s"' % sqs.query.clean(value)
            sqs = sqs.narrow(u'value_exact:%s' % query)
        if self.categories:
            query = None
            for category in self.categories:
                if query:
                    query += u' AND '
                else:
                    query = u''
                query += u'"%s"' % sqs.query.clean(category)
            sqs = sqs.narrow(u'category_exact:%s' % query)

        if not hasattr(self.data.get, 'order_by'):
            return sqs
        try:
            if int(self.data.get('order_by')[0]) == '2':
                return sqs.order_by('-price')
            elif int(self.data.get('order_by')[0]) == '1':
                return sqs.order_by('price')
        except:
            return sqs


# Класс для вывода категорий и фасетов к ним единственное отличие от верхнего класса - это нет переменной q
# И здесь не должно быть фасетных категорий или вернее они должны быть выше
class FacetedProductListing(FacetedSearchForm):

    def __init__(self, *args, **kwargs):

        data = dict(kwargs.get("data", []))
        self.conds = data.get('cond', [])
        self.brands = data.get('brand', [])
        self.cars = data.get('car', [])
        self.car_models = data.get('car_model', [])
        self.fuels = data.get('fuel', [])
        self.values = data.get('value', [])
        self.prices = data.get('prices', []),
        self.categories = data.get('category', [])


        super().__init__(*args, **kwargs)

    def search(self):
        #print(self.cleaned_data.get("q"))
        if not self.cleaned_data.get("q") or self.cleaned_data.get("q") == '' or self.cleaned_data.get("q") == 'null' or self.cleaned_data.get("q") is None:
            #return self.no_query_found()
            sqs = self.searchqueryset.filter(price__gt=MIN_PRICE)
            pass
        else:
            #sqs = super().search()

            sqs = self.searchqueryset.auto_query(self.cleaned_data.get("q"), fieldname='name')




        if self.car_models:
            query = None
            for car_model in self.car_models:
                if query:
                    query += u' AND '
                else:
                    query = u''
                query += u'"%s"' % sqs.query.clean(car_model)
            sqs = sqs.narrow(u'car_model_exact:%s' % query)


        if self.conds:
            query = None
            for cond in self.conds:
                if query:
                    query += u' AND '
                else:
                    query = u''
                query += u'"%s"' % sqs.query.clean(cond)
            sqs = sqs.narrow(u'cond_exact:%s' % query)

        if self.brands:
            query = None
            for brand in self.brands:
                if query:
                    query += u' AND '
                else:
                    query = u''
                query += u'"%s"' % sqs.query.clean(brand)
            sqs = sqs.narrow(u'brand_exact:%s' % query)

        if self.cars:
            query = None
            for car in self.cars:
                if query:
                    query += u' AND '
                else:
                    query = u''
                query += u'"%s"' % sqs.query.clean(car)
            sqs = sqs.narrow(u'car_exact:%s' % query)

        if self.fuels:
            query = None
            for fuel in self.fuels:
                if query:
                    query += u' AND '
                else:
                    query = u''
                query += u'"%s"' % sqs.query.clean(fuel)
            sqs = sqs.narrow(u'fuel_exact:%s' % query)

        if self.values:
            query = None
            for value in self.values:
                if query:
                    query += u' AND '
                else:
                    query = u''
                query += u'"%s"' % sqs.query.clean(value)
            sqs = sqs.narrow(u'value_exact:%s' % query)
        if self.categories:
            query = None
            for category in self.categories:
                if query:
                    query += u' AND '
                else:
                    query = u''
                query += u'"%s"' % sqs.query.clean(category)
            sqs = sqs.narrow(u'category_exact:%s' % query)

        if self.data.get('order_by') is None:
            return sqs.filter(price__gt=MIN_PRICE)

        if self.data.get('order_by') == '2':
            return sqs.filter(price__gt=MIN_PRICE).order_by('-price')

        elif self.data.get('order_by') == '1':
            return sqs.filter(price__gt=MIN_PRICE).order_by('price')

# Класс для вывода категорий и фасетов к ним единственное отличие от верхнего класса - это нет переменной q
# И здесь не должно быть фасетных категорий или вернее они должны быть выше
class FacetedProductListingSubcat(FacetedSearchForm):

    def __init__(self, *args, **kwargs):
        slug = kwargs.pop('slug')
        self.slug_id = [kwargs.pop('slug_id'),]
        self.id_list = kwargs.pop('id_list')
        self.rus_name = kwargs.pop('rus_name')
        data = dict(kwargs.get("data", []))
        self.conds = data.get('cond', [])
        self.brands = data.get('brand', [])
        self.cars = data.get('car', [])
        self.car_models = data.get('car_model', [])
        self.fuels = data.get('fuel', [])
        self.values = data.get('value', [])
        self.prices = data.get('prices', []),
        self.categories = data.get('category', [])

        super().__init__(*args, **kwargs)

    def search(self):
        #print(self.cleaned_data.get("q"))
        if not self.cleaned_data.get("q") or self.cleaned_data.get("q") == '' or self.cleaned_data.get("q") == 'null' or self.cleaned_data.get("q") is None:
            #return self.no_query_found()
            sqs = self.searchqueryset.filter(price__gt=MIN_PRICE)
        else:
            sqs = super().search()

        if self.car_models:
            query = None
            for car_model in self.car_models:
                if query:
                    query += u' AND '
                else:
                    query = u''
                query += u'"%s"' % sqs.query.clean(car_model)
            sqs = sqs.narrow(u'car_model_exact:%s' % query)

        if self.conds:
            query = None
            for cond in self.conds:
                if query:
                    query += u' AND '
                else:
                    query = u''
                query += u'"%s"' % sqs.query.clean(cond)
            sqs = sqs.narrow(u'cond_exact:%s' % query)

        if self.brands:
            query = None
            for brand in self.brands:
                if query:
                    query += u' AND '
                else:
                    query = u''
                query += u'"%s"' % sqs.query.clean(brand)
            sqs = sqs.narrow(u'brand_exact:%s' % query)

        if self.cars:
            query = None
            for car in self.cars:
                if query:
                    query += u' AND '
                else:
                    query = u''
                query += u'"%s"' % sqs.query.clean(car)
            sqs = sqs.narrow(u'car_exact:%s' % query)

        if self.fuels:
            query = None
            for fuel in self.fuels:
                if query:
                    query += u' AND '
                else:
                    query = u''
                query += u'"%s"' % sqs.query.clean(fuel)
            sqs = sqs.narrow(u'fuel_exact:%s' % query)

        if self.values:
            query = None
            for value in self.values:
                if query:
                    query += u' AND '
                else:
                    query = u''
                query += u'"%s"' % sqs.query.clean(value)
            sqs = sqs.narrow(u'value_exact:%s' % query)
        if self.categories:
            query = None
            for category in self.categories:
                if query:
                    query += u' AND '
                else:
                    query = u''
                query += u'"%s"' % sqs.query.clean(category)
            sqs = sqs.narrow(u'category_exact:%s' % query)

        if self.data.get('order_by') is None:
            return sqs.filter(price__gt=MIN_PRICE).filter(cat_id__in=self.id_list)

        if self.data.get('order_by') == '2':
            return sqs.filter(price__gt=MIN_PRICE).filter(cat_id__in=self.id_list).order_by('-price')

        elif self.data.get('order_by') == '1':
            return sqs.filter(price__gt=MIN_PRICE).filter(cat_id__in=self.id_list).order_by('price')







