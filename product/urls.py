from django.urls import path

from .views import (
    ProductDetailView,
    ProductDetailSlugView,
    FacetedListCat,
    FacetedListSubCat,
    FacetedListSubSubCat,
    FacetedListSubSubCatLast,
    FacetedListSubSubCatLastSuper,
)

urlpatterns = [
    path('', FacetedListCat.as_view(), name='products'),
    path('subcat/<slug:slug>/', FacetedListSubCat.as_view(), name='subcat'),
    path('last/<slug:slug>/', FacetedListSubSubCatLast.as_view(), name='last'),
    path('supercat/<slug:slug>/', FacetedListSubSubCatLastSuper.as_view(), name='supercat'),
    path('cat/<slug:slug>/', FacetedListSubSubCat.as_view(), name='subsubcat'),
    path('detail/<slug:slug>/', ProductDetailSlugView.as_view(), name='detailed'),
    path('detail2/<int:pk>/', ProductDetailView.as_view(), name='detailed_id'),

]
