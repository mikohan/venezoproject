import datetime
from django.utils import timezone
from haystack import indexes
from haystack.fields import CharField


from .models import AlegroGoodsSpec


class ProductIndex(indexes.SearchIndex, indexes.Indexable):

    # template_name='/home/manhee/anaconda3/envs/djviews1/src/templates/product_text.txt'

    text = indexes.EdgeNgramField(model_attr='name', document=True, use_template=True)
    category                = indexes.CharField(model_attr='cat_id__rus_name', faceted=True)
    name                    = indexes.EdgeNgramField(model_attr='name')
    price                   = indexes.IntegerField(model_attr='price')
    cond                    = indexes.CharField(model_attr='cond', faceted=True)
    brand                   = indexes.CharField(model_attr='brand', faceted=True)
    car                     = indexes.CharField(model_attr='car', faceted=True)
    car_model               = indexes.CharField(model_attr='car_model', faceted=True)
    cat_n                   = indexes.CharField(model_attr='cat_n')
    color                   = indexes.CharField(model_attr='color')
    fuel                    = indexes.CharField(model_attr='fuel', faceted=True)
    value                   = indexes.CharField(model_attr='value', faceted=True)
    cat_id                  = indexes.IntegerField(model_attr='cat_id__id')



    # for auto complete
    content_auto = indexes.EdgeNgramField(model_attr='name')

    # Spelling suggestions
    suggestions = indexes.FacetCharField()


    def get_model(self):
        return AlegroGoodsSpec

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()
