from django.urls import path
from . import views

urlpatterns = [
    path('place-order/', views.place_order, name='place_order'),
    path('razorpay-verify/', views.razorpay_verify, name='razorpay_verify'),
    path('order-complete/', views.order_complete, name='order_complete'),
]
