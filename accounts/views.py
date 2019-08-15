from django.shortcuts import render
from django.contrib.auth import authenticate, login, get_user_model
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import LoginForm, RegisterForm, GuestForm
from django.utils.http import is_safe_url
from .models import GuestEmail
from addresses.models import Address
from billing.models import BillingProfile
from orders.models import Order
def guest_register_view(request):
    form = GuestForm(request.POST or None)
    form_register = RegisterForm(request.POST or None)
    context = {
        'form_login': form,
        'title': 'Login page',
        'form_register': form_register,
        'page_title': 'Страница Авторизации',
    }
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post or None
    if form.is_valid():
        email = form.cleaned_data.get('email')
        new_guest_email = GuestEmail.objects.create(email=email)
        request.session['guest_email_id'] = new_guest_email.id
        if is_safe_url(redirect_path, request.get_host()):
            return redirect(redirect_path)
        else:
            return redirect('/register/')
    return redirect('/register/')


def login_page(request):
    form = LoginForm(request.POST or None)
    form_register = RegisterForm(request.POST or None)
    context = {
        'form_login': form,
        'title': 'Login page',
        'form_register': form_register,
        'page_title': 'Страница Авторизации',
    }
    #print(request.user.is_authenticated)
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post or None
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            try:
                del request.session['guest_email_id']
            except:
                pass
            if is_safe_url(redirect_path, request.get_host()):
                return redirect(redirect_path)
            else:
                return redirect('/')
        else:
            print('Error')

    if form_register.is_valid():
        print(form_register.cleaned_data)
        username = form_register.cleaned_data.get('username')
        email = form_register.cleaned_data.get('email')
        password = form_register.cleaned_data.get('password')
        new_user = User.objects.create_user(username, email, password)
        #print('on login page', new_user)
        return redirect('my-account', new_user)


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
        #print('on register page', new_user)
        return redirect('my-account', new_user)


    return render(request, 'auth/login.html', context)

def profile_page(request, new_user=''):
    if request.user.is_authenticated:
        new_user = request.user
        billing_profile = BillingProfile.objects.get(user_id=new_user.pk)
        address = Address.objects.filter(billing_profile=billing_profile.pk)
        orders = Order.objects.filter(billing_profile=billing_profile.pk)
        print(orders, 'in profile')
        context = {'user': new_user,
                    'address': address,
                    'orders': orders,
                }
        return render(request, 'accounts/my_account.html', context)
    print(new_user, 'in profile')
    return render(request, 'accounts/my_account.html', context)
