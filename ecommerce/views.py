from django.contrib.auth import authenticate, login, get_user_model
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import ContactForm, LoginForm, RegisterForm
from product.models import CatSubRus, AlegroGoods, SuperCat, FeaturedProduct
from blog.models import BlogModel
from carts.models import Cart
from django.conf import settings

def home_page(request):
    qs = CatSubRus.objects.filter(parent_id=0)
    select_cars = FeaturedProduct.objects.filter(on_main=1).select_related('product_id').all()
    select_cars2 = FeaturedProduct.objects.filter(on_main=1).select_related('product_id').all()
    select_cars3 = FeaturedProduct.objects.filter(on_main=1).select_related('product_id').all()

    select_new_arrivals = FeaturedProduct.objects.filter(on_main=2).select_related('product_id').all()

    select_construct = FeaturedProduct.objects.filter(on_main=3).select_related('product_id').all()
    select_construct2 = FeaturedProduct.objects.filter(on_main=3).select_related('product_id').all()
    select_construct3 = FeaturedProduct.objects.filter(on_main=3).select_related('product_id').all()

    select_misc = FeaturedProduct.objects.filter(on_main=5).select_related('product_id').all()
    select_misc2 = FeaturedProduct.objects.filter(on_main=5).select_related('product_id').all()
    select_misc3 = FeaturedProduct.objects.filter(on_main=5).select_related('product_id').all()

    select_featured = FeaturedProduct.objects.filter(on_main=6).select_related('product_id').all()
    select_most_viewed = FeaturedProduct.objects.filter(on_main=7).select_related('product_id').all()
    select_bestseller = FeaturedProduct.objects.filter(on_main=8).select_related('product_id')
    blogs = BlogModel.objects.all().order_by('-publish')[:4]
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    context = {
        'CDN_SERVER': settings.CDN_SERVER,
        'name': 'Home page',
        'categories':qs,
        'cars_features' : select_cars,
        'cars_features2': select_cars2,
        'cars_features3': select_cars3,
        'construction_machines' : select_construct,
        'construction_machines2': select_construct2,
        'construction_machines3': select_construct3,
        'new_arrivals' : select_new_arrivals,
        'misc_parts' : select_misc,
        'misc_parts2': select_misc2,
        'misc_parts3': select_misc3,
        'featured' : select_featured,
        'most_viewed' : select_most_viewed,
        'bestseller' : select_bestseller,
        'cats' : qs,
        'blogs' : blogs,
        'cart' : cart_obj,
    }
    return render(request, 'home/home_page.html', context)


def about_page(request):
    context = {'name': 'О компании',
               'page_title': 'Страница о Компании',
               }
    return render(request, 'about/about.html', context)

def warraty_page(request):
    context = {'name': 'Гарантии',
               'page_title': 'Гарантии на запчасти',
               }
    return render(request, 'about/warranty.html', context)

def payment_page(request):
    context = {'name': 'Оплата',
               'page_title': 'Способы оплаты',
               }
    return render(request, 'about/payment.html', context)

def delivery_page(request):
    context = {'name': 'О компании',
               'page_title': 'Страница Доставка',
               }
    return render(request, 'delivery/delivery.html', context)


def contact_page(request):
    contact_form = ContactForm(request.POST or None)
    context = {'name': 'Contact page',
               'form': contact_form,
               'page_title': 'Контакты',
               }
    if contact_form.is_valid():
        print(contact_form.cleaned_data)

    if request.method == 'POST':
        print(request.POST)
        print(request.POST.get('email'))
    return render(request, 'contact/contacts.html', context)


def login_page(request):
    form = LoginForm(request.POST or None)
    form_register = RegisterForm(request.POST or None)
    context = {
        'form_login': form,
        'title': 'Login page',
        'form_register': form_register,
        'page_title': 'Страница Авторизации',
    }
    print(request.user.is_authenticated)
    if form.is_valid():
        print(form.cleaned_data)
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
           # context['form'] = LoginForm
            return redirect('/login')
        else:
            print('Error')

    if form_register.is_valid():
        print(form_register.cleaned_data)
        username = form_register.cleaned_data.get('username')
        email = form_register.cleaned_data.get('email')
        password = form_register.cleaned_data.get('password')
        new_user = User.objects.create_user(username, email, password)
        print(new_user)


    return render(request, 'auth/login.html', context)

User = get_user_model()

def register_page(request):
    form = RegisterForm(request.POST or None)
    context = {
        'form_register' : form
    }
    if form.is_valid():
        print(form.cleaned_data)
        username = form.cleaned_data.get('username')
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        new_user = User.objects.create_user(username, email, password)
        print(new_user)


    return render(request, 'auth/login.html', context)
