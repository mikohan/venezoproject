from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from .models import Cart
from product.models import AlegroGoods
from orders.models import Order
from accounts.forms import LoginForm, GuestForm
from billing.models import BillingProfile
from accounts.models import GuestEmail
from addresses.forms import AddressForm
from addresses.models import Address
from django.core.mail import send_mail
from django.http import JsonResponse
from django.conf import settings


def cart_detail_api_view(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    products = [{
        'id': x.id,
        'name': x.name,
        'price': x.price
    } for x in cart_obj.products.all()]
    cart_data = {'products': products, 'subtotal': cart_obj.subtotal, 'total': cart_obj.total}
    return JsonResponse(cart_data)


def view_cart(request, pk):
    cart_obj = Cart.objects.just_get(request, pk)
    if not request.user.is_authenticated:
        return redirect('home')
    products = [{
        'id': x.id,
        'name': x.name,
        'price': x.price
    } for x in cart_obj.products.all()]
    context = {
            'cart': cart_obj,
            'porducts': products,
            'CDN_SERVER': settings.CDN_SERVER,
            }
    return render(request, 'shop/cart.html', context)

def cart_home(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)


    return render(request, "shop/cart.html", {'cart' : cart_obj, 'CDN_SERVER': settings.CDN_SERVER })



def cart_update(request):
    product_id = request.POST.get('product_id')

    #print(product_id)
    if product_id is not None:
        try:
            product_obj = AlegroGoods.objects.get(id=product_id)
        except AlegroGoods.DoesNotExist:
            print('Товар закончился')
            return redirect('cart:carts')
        product_obj = AlegroGoods.objects.get(id=product_id)
        cart_obj, new_obj = Cart.objects.new_or_get(request)
        if product_obj in cart_obj.products.all():
            cart_obj.products.remove(product_obj)
            added = False
        else:
            cart_obj.products.add(product_obj)
            added = True
        request.session['cart_items'] = cart_obj.products.count()
        request.session['cart_total'] = cart_obj.subtotal

        products = [{
            'id': x.id,
            'name': x.name,
            'price': x.price
        } for x in cart_obj.products.all()]

        request.session['cart_products'] = products
        if request.is_ajax():
            json_data = {
                'added':added,
                'removed': not added,
                'cartItemCount' : cart_obj.products.count()
            }
            request.session['cart_products'] = products
            return JsonResponse(json_data)


    #return redirect('cart:carts')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def checkout(request):
    cart_obj, cart_created = Cart.objects.new_or_get(request)
    order_obj = None
    if cart_created or cart_obj.products.count() == 0:
        return redirect('cart:carts')

    login_form = LoginForm()
    guest_form = GuestForm()
    address_form = AddressForm()
    billing_address_form = AddressForm()
    billing_address_id = request.session.get('billing_address_id', None)
    shipping_address_id = request.session.get('shipping_address_id', None)

    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
    address_qs = None

    if billing_profile is not None:
        if request.user.is_authenticated:
            address_qs = Address.objects.filter(billing_profile=billing_profile)

        order_obj, order_obj_created = Order.objects.new_or_get(billing_profile, cart_obj)
        if shipping_address_id:
            order_obj.shipping_address = Address.objects.get(id=shipping_address_id)

            del request.session['shipping_address_id']
        if billing_address_id:
            order_obj.billing_address = Address.objects.get(id=billing_address_id)
            del request.session['billing_address_id']
        if billing_address_id or shipping_address_id:
            order_obj.save()

    if request.method == 'POST':
        is_done = order_obj.check_done()
        if is_done:
            ## Sending emails
            print(order_obj.shipping_address.telephone)
            to_email = str(billing_profile)
            send_mail(
                'Ваш заказ номер {} на сумму {} отправлен'.format(order_obj.order_id, cart_obj.total),
                'Спасибо за заказ! Менеджер свяжется с Вами в ближайшее рабочее время по телефону {}. Номер Вашего заказа {}'.format(order_obj.shipping_address.telephone, order_obj.order_id),
                'angara99@gmail.com', # from email
                [to_email], # to email
                fail_silently=False,
            )
            order_obj.mark_paid()
            request.session['cart_items'] = 0
            del request.session['cart_id']

            return redirect('cart:success')

    context = {
        'object': order_obj,
        'billing_profile': billing_profile,
        'login_form' : login_form,
        'guest_form' : guest_form,
        'address_form' : address_form,
        'billing_address_form' : billing_address_form,
        'address_qs' : address_qs,
        'CDN_SERVER': settings.CDN_SERVER,
    }
    return render(request, 'shop/checkout.html', context)

def checkout_done_view(request):
    context = {}
    return render(request, 'shop/success.html', context)
