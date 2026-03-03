# Create your views here.
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from carts.models import CartItem
from .forms import OrderForm
import datetime
from .models import Order, Payment, OrderProduct
import json
from store.models import Product
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

import razorpay
from django.conf import settings
from orders.models import Payment
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required   
from django.shortcuts import get_object_or_404

@csrf_exempt
@login_required
def razorpay_verify(request):
    if request.method == "POST":
        data = json.loads(request.body)

        razorpay_payment_id = data.get("razorpay_payment_id")
        razorpay_order_id = data.get("razorpay_order_id")
        razorpay_signature = data.get("razorpay_signature")

        client = razorpay.Client(
            auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
        )

        #  Verify signature
        try:
            client.utility.verify_payment_signature({
                "razorpay_order_id": razorpay_order_id,
                "razorpay_payment_id": razorpay_payment_id,
                "razorpay_signature": razorpay_signature
            })
        except:
            return JsonResponse({"error": "Signature verification failed"}, status=400)

        #  Get payment
        payment = Payment.objects.get(razorpay_order_id=razorpay_order_id)
        payment.razorpay_payment_id = razorpay_payment_id
        payment.razorpay_signature = razorpay_signature
        payment.status = True
        payment.save()

        #  Get EXACT order linked to this payment
        order = Order.objects.get(payment=payment)
        order.is_ordered = True
        order.status = "Completed"
        order.save()

        #  Move cart → order products
        cart_items = CartItem.objects.filter(user=request.user)

        for item in cart_items:
            order_product = OrderProduct.objects.create(
                order=order,
                payment=payment,
                user=request.user,
                product=item.product,
                quantity=item.quantity,
                product_price=item.product.get_final_price(),
                ordered=True
            )
            order_product.variations.set(item.variations.all())

            # reduce stock
            item.product.stock -= item.quantity
            item.product.save()

        #  Clear cart
        cart_items.delete()

        #  RETURN EXACT KEYS EXPECTED BY JS
        return JsonResponse({
            "order_number": order.order_number,
            "payment_id": payment.razorpay_payment_id
        })


@login_required
def place_order(request):
    current_user = request.user

    cart_items = CartItem.objects.filter(user=current_user)
    if not cart_items.exists():
        return redirect('store')

    total = 0
    quantity = 0
    tax = 0

    for item in cart_items:
        total += item.product.get_final_price() * item.quantity
        quantity += item.quantity

    tax = (2 * total) / 100
    grand_total = total + tax

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():

            # 1️ CREATE ORDER
            order = Order.objects.create(
                user=current_user,
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                phone=form.cleaned_data['phone'],
                email=form.cleaned_data['email'],
                address_line_1=form.cleaned_data['address_line_1'],
                address_line_2=form.cleaned_data['address_line_2'],
                country=form.cleaned_data['country'],
                state=form.cleaned_data['state'],
                city=form.cleaned_data['city'],
                order_note=form.cleaned_data['order_note'],
                order_total=grand_total,
                tax=tax,
                ip=request.META.get('REMOTE_ADDR'),
            )

            # Generate order number
            order.order_number = f"{order.id}{order.created_at.strftime('%Y%m%d')}"
            order.save()

            # 2️ CREATE RAZORPAY ORDER
            client = razorpay.Client(
                auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
            )

            razorpay_order = client.order.create({
                "amount": int(grand_total * 100),  # paise
                "currency": "INR",
                "payment_capture": 1
            })

            # 3️ CREATE PAYMENT
            payment = Payment.objects.create(
                user=current_user,
                razorpay_order_id=razorpay_order['id'],
                amount=grand_total,
                status=False
            )

            #   THIS LINE WAS MISSING 
            order.payment = payment
            order.save()

            # 4️ RENDER PAYMENT PAGE
            context = {
                'order': order,
                'cart_items': cart_items,
                'total': total,
                'tax': tax,
                'grand_total': grand_total,
                'razorpay_key': settings.RAZORPAY_KEY_ID,
                'razorpay_order_id': razorpay_order['id'],
                'amount': int(grand_total * 100),
            }

            return render(request, 'orders/payments.html', context)

    return redirect('checkout')


@login_required
def order_complete(request):
    order_number = request.GET.get('order_number')
    payment_id = request.GET.get('payment_id')

    #  Prevent direct access
    if not order_number or not payment_id:
        return redirect('store')

    order = get_object_or_404(
        Order,
        order_number=order_number,
        is_ordered=True
    )

    ordered_products = OrderProduct.objects.filter(order=order)

    subtotal = 0
    for item in ordered_products:
        subtotal += item.product_price * item.quantity

    context = {
        'order': order,
        'ordered_products': ordered_products,
        'order_number': order.order_number,
        'transID': payment_id,
        'payment': order.payment,
        'subtotal': subtotal,
    }

    return render(request, 'orders/order_complete.html', context)


    
