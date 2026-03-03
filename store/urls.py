from django.urls import path
from . import views
from carts import views as cart_views


urlpatterns = [
    path('', views.home, name='home'),
    path('shop/', views.store, name='store'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('cart/', cart_views.cart, name='cart'),
    path('add_cart/<int:product_id>/', views.add_cart, name='add_cart'),
    path('category/<slug:category_slug>/', views.store, name='products_by_category'),
    path('category/<slug:category_slug>/<slug:product_slug>/', views.product_detail, name='product_detail'),
    path('search/', views.search, name='search'),
    path('submit_review/<int:product_id>/', views.submit_review, name='submit_review'),
]
