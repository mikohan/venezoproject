from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

from .views import home_page, about_page, contact_page, delivery_page, warraty_page, payment_page, send_mail
from product.views import  autocomplete

from product import urls as prod_urls
from blog import urls as blog_urls
from carts import urls as cart_urls

from product.views import FacetedSearchView, ProductDetailView
from accounts.views import login_page, register_page, guest_register_view, profile_page
from django.contrib.auth.views import LogoutView
from addresses.views import checkout_address_create_view, checkout_address_reuse_view
from carts.views import cart_detail_api_view
from django.contrib.sitemaps import views
from django.contrib.sitemaps import GenericSitemap
from product.models import AlegroGoods
from django.utils import timezone
from .sitemaps import ProductSitemaps, CategoriesSitemaps, BlogSitemaps
sitemaps = {
        'categories': CategoriesSitemaps,
        'products': ProductSitemaps,
        'blog': BlogSitemaps,
        }





urlpatterns = [
    #path(r'^favicon.+$', RedirectView.as_view(url='/static/img/favicon-venezo.png')),
    path('admin/', admin.site.urls),
    path('', home_page, name='home'),
    path('about/', about_page, name='about'),
    path('payment/', payment_page, name='payment'),
    path('warranty/', warraty_page, name='warranty'),
    path('contacts/', contact_page, name='contacts'),
    path('login/', login_page, name='login'),
    path('checkout/address/create/', checkout_address_create_view, name='checkout_address_create'),
    path('checkout/address/reuse/', checkout_address_reuse_view, name='checkout_address_reuse'),
    path('register/guest/', guest_register_view, name='guest_register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('api/cart/',cart_detail_api_view , name='api-cart'),
    path('register/', register_page, name='register'),
    path('myaccount/', profile_page, name='myaccount'),
    path('products/', include(prod_urls), name='products'),
   # path('spec/', include(prod_urls), name='spec'),
    path('blog/', include(blog_urls), name='blog'),
    path('cart/', include((cart_urls, 'carts'), namespace='cart')),
    path('delivery/', delivery_page, name='delivery'),
    path('find/', FacetedSearchView.as_view(), name='haystack_search'),
    path('search/autocomplete/', autocomplete),
    path('sitemap.xml', views.index, {'sitemaps': sitemaps}),
    path('sitemap-<section>.xml', views.sitemap, {'sitemaps': sitemaps }, name='django.contrib.sitemaps.views.sitemap'),
    path('sendmail/', send_mail, name='send_mail'),


]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
