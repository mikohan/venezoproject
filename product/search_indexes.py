import datetime
from django.utils import timezone
from haystack import indexes
from haystack.fields import CharField


from .models import AlegroGoods


class ProductIndex(indexes.SearchIndex, indexes.Indexable):

    # template_name='/home/manhee/anaconda3/envs/djviews1/src/templates/product_text.txt'

    text = indexes.EdgeNgramField(model_attr='name', document=True, use_template=True)
    category                = indexes.CharField(model_attr='cat_id__rus_name', faceted=True)
    name                    = indexes.EdgeNgramField(model_attr='name')
    price                   = indexes.IntegerField(model_attr='price')
    cond                    = indexes.CharField(model_attr='cond', null=True, faceted=True)
    brand                   = indexes.CharField(model_attr='brand', null=True, faceted=True)
    car                     = indexes.CharField(model_attr='car', null=True, faceted=True)
    car_model               = indexes.CharField(model_attr='car_model', null=True, faceted=True)
    cat_n                   = indexes.CharField(model_attr='cat_n', null=True,)
    color                   = indexes.CharField(model_attr='color', null=True,)
    fuel                    = indexes.CharField(model_attr='fuel', null=True, faceted=True)
    value                   = indexes.CharField(model_attr='value', null=True, faceted=True)
    cat_id                  = indexes.IntegerField(model_attr='cat_id__id')
    subsubcat_id            = indexes.CharField(model_attr='subsubcat_id', null=True)



    # for auto complete
    #content_auto = indexes.EdgeNgramField(model_attr='name')
    content_auto = indexes.EdgeNgramField(model_attr='cat_id__rus_name')

    # Spelling suggestions
    suggestions = indexes.FacetCharField()


    def get_model(self):
        return AlegroGoods

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()
