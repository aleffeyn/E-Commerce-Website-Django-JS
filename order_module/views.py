import time

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from django.urls import reverse

from order_module.models import Order, OrderDetail
from product_module.models import Product
from django.conf import settings
import requests
import json

# Create your views here.


# ? sandbox merchant
if settings.SANDBOX:
    sandbox = 'sandbox'
else:
    sandbox = 'www'

ZP_API_REQUEST = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
ZP_API_VERIFY = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
ZP_API_STARTPAY = f"https://{sandbox}.zarinpal.com/pg/StartPay/"

amount = 1000  # Rial / Required
description = "جهت نهایی کردن خرید کاربر"  # Required
phone = 'YOUR_PHONE_NUMBER'  # Optional
# Important: need to edit for realy server.
CallbackURL = 'http://127.0.0.1:8080/order/verify/'



def add_product_to_order(request: HttpRequest):
    product_id = int(request.GET.get('product_id'))
    count = int(request.GET.get('count'))
    if count < 1:
        return JsonResponse({
            'status': 'count_not_valid',
            'title' : 'اعلان',
            'message' : 'تعداد وارد شده معتبر نمی باشد',
            'icon' : 'error',
            'confirm_button_text' : 'اوکی'
        })
    if request.user.is_authenticated:
        product = Product.objects.filter(id=product_id, is_active=True, is_delete=False).first()
        if product is not None:
            current_order, created = Order.objects.get_or_create(is_paid=False, user_id=request.user.id)
            current_order_detail = current_order.orderdetail_set.filter(product_id=product_id).first()
            if current_order_detail is not None:
                current_order_detail.count += int(count)
                current_order_detail.save()
            else:
                new_detail = OrderDetail(order_id=current_order.id, product_id=product_id, count=count)
                new_detail.save()

            return JsonResponse({
                'title': 'محصول با موفقیت به سبد خرید شما اضافه شد',
                'status': 'success',
                'message': 'آیا می خواهید خرید خود را نهایی کنید؟',
                'icon': 'info',
                'confirm_button_text': 'نهایی کردن سفارش',
                'cancel_button_text': 'ادامه خرید',
            })

        else:
            return JsonResponse({
                'status': 'product_not_found',
                'title': 'اعلان',
                'message': 'محصول مورد نظر یافت نشد',
                'icon': 'error',
            })

    else:
        return JsonResponse({
            'status': 'not_logged_in',
            'title': 'اعلان',
            'message': 'برای اضافه کردن محصول به سبد خرید خود می بایست لاگین باشید',
            'icon': 'warning',
            'confirm_button_text': 'ورود به سایت'
        })

@login_required
def send_request(request):
    current_order, created = Order.objects.prefetch_related('orderdetail_set').get_or_create(is_paid=False,user_id=request.user.id)
    total_amount = current_order.calculate_total_amount()
    if total_amount == 0:
        return reverse('user_basket')
    data = {
        "MerchantID": settings.MERCHANT,
        "Amount": total_amount * 10,
        "Description": description,
        "CallbackURL": CallbackURL,
    }
    data = json.dumps(data)
    # set content length by data
    headers = {'content-type': 'application/json', 'content-length': str(len(data))}
    try:
        response = requests.post(ZP_API_REQUEST, data=data, headers=headers, timeout=10)

        if response.status_code == 200:
            response = response.json()
            if response['Status'] == 100:
                return {'status': True, 'url': ZP_API_STARTPAY + str(response['Authority']),
                        'authority': response['Authority']}
            else:
                return {'status': False, 'code': str(response['Status'])}
        return response

    except requests.exceptions.Timeout:
        return {'status': False, 'code': 'timeout'}
    except requests.exceptions.ConnectionError:
        return {'status': False, 'code': 'connection error'}

@login_required
def verify(authority, request):
    current_order, created = Order.objects.prefetch_related('orderdetail_set').get_or_create(is_paid=False,user_id=request.user.id)
    total_amount = current_order.calculate_total_amount()
    order_details = current_order.orderdetail_set.all()

    data = {
        "MerchantID": settings.MERCHANT,
        "Amount": total_amount * 10,
        "Authority": authority,
    }
    data = json.dumps(data)
    # set content length by data
    headers = {'content-type': 'application/json', 'content-length': str(len(data))}
    response = requests.post(ZP_API_VERIFY, data=data, headers=headers)

    if response.status_code == 200:
        response = response.json()
        if response['Status'] == 100:
            for order_detail in order_details:
                order_detail.final_price = order_detail.product.price * order_detail.count
                order_detail.save()
            current_order.is_paid = True
            current_order.payment_date = time.time()
            current_order.save()
            context = {
                'status': True,
                'RefID': response['RefID'],
                'success' : "پرداخت با موفقیت انجام شد"
            }
            return render(request, 'order_module/payment_result.html', context)
        else:
            context = {'status': False,
                       'code': str(response['Status']),
                       'error' : 'پرداخت با مشکل مواجه شد یا کاربر روند پرداخت خود را کنسل کرد'
                       }
            return render(request, 'order_module/payment_result.html', context)
    return response
