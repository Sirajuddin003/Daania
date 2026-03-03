from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, ReviewRating, ProductGallery
from category.models import Category
from carts.models import Cart, CartItem
from django.db.models import Q
from django.http import JsonResponse
from carts.views import _cart_id
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse
from .forms import ReviewForm
from orders.models import OrderProduct
from .models import HomePage, Ingredient, FollowGallery
from .models import AboutPage
from django.contrib import messages

def home(request):
    products = Product.objects.filter(is_available=True).order_by('-created_date')[:9]  # featured products
    context = {
        'products': products,
    }
    return render(request, 'home.html', context)


def store(request):
    products = Product.objects.filter(is_available=True).order_by('id')
    categories = Category.objects.all()

    # ================= CATEGORY FILTER (FIXED) =================
    category_slug = request.GET.get('category')
    if category_slug:
        products = products.filter(category__slug=category_slug)

    # ================= SEARCH FILTER =================
    keyword = request.GET.get('keyword')
    if keyword:
        products = products.filter(
            Q(product_name__icontains=keyword) |
            Q(description__icontains=keyword)
        )

    # ================= PRICE FILTER =================
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    if min_price:
        products = products.filter(price__gte=min_price)

    if max_price:
        products = products.filter(price__lte=max_price)

    # ================= PAGINATION =================
    paginator = Paginator(products, 6)
    page = request.GET.get('page')

    try:
        paged_products = paginator.page(page)
    except PageNotAnInteger:
        paged_products = paginator.page(1)
    except EmptyPage:
        paged_products = paginator.page(paginator.num_pages)

    context = {
        'products': paged_products,
        'product_count': products.count(),
        'categories': categories,
        'min_price': min_price,
        'max_price': max_price,
        'keyword': keyword,
        'selected_category': category_slug,
    }

    return render(request, 'store/store.html', context)


def contact(request):
    if request.method == 'POST':
        # handle form later
        pass
    return render(request, 'contact.html')



def about(request):
    about_page = AboutPage.objects.first()
    context = {
        'about_page': about_page,
    }
    return render(request, 'about.html', context)



def product_detail(request, category_slug, product_slug):

    single_product = get_object_or_404(
        Product,
        category__slug=category_slug,
        slug=product_slug
    )

    # PRODUCT GALLERY
    product_gallery = ProductGallery.objects.filter(product=single_product)

    # REVIEWS
    reviews = ReviewRating.objects.filter(
        product=single_product,
        status=True
    )

    #  RELATED PRODUCTS (KEY PART)
    related_products = Product.objects.filter(
        category=single_product.category,
        is_available=True
    ).exclude(id=single_product.id)[:4]

    context = {
        'single_product': single_product,
        'product_gallery': product_gallery,
        'reviews': reviews,
        'related_products': related_products,
    }

    return render(request, 'store/product_detail.html', context)




def add_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    #  If product is out of stock
    if product.stock <= 0:
        return JsonResponse({
            "success": False,
            "message": "This product is out of stock"
        }, status=400)

    cart, _ = Cart.objects.get_or_create(cart_id=_cart_id(request))

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product
    )

    #  STOCK LIMIT CHECK
    if not created:
        if cart_item.quantity < product.stock:
            cart_item.quantity += 1
            cart_item.save()
        else:
            return JsonResponse({
                "success": False,
                "message": "Maximum available stock already added"
            }, status=400)
    else:
        # First time add → quantity = 1
        cart_item.quantity = 1
        cart_item.save()

    cart_count = CartItem.objects.filter(cart=cart).count()

    return JsonResponse({
        "success": True,
        "cart_count": cart_count,
        "message": "Item added to your cart"
    })


def search(request):
    products = Product.objects.none()   # ✅ ALWAYS define first

    keyword = request.GET.get('keyword', '')
    category_slug = request.GET.get('category', '')

    if category_slug:
        try:
            category = Category.objects.get(slug=category_slug)
            products = Product.objects.filter(category=category, is_available=True)
        except Category.DoesNotExist:
            products = Product.objects.none()

    if keyword:
        products = products.filter(
            product_name__icontains=keyword
        )

    context = {
        'products': products,
    }

    return render(request, 'store/store.html', context)


def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
            reviews = ReviewRating.objects.get(user__id=request.user.id, product__id=product_id)
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            messages.success(request, 'Thank you! Your review has been updated.')
            return redirect(url)
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(request, 'Thank you! Your review has been submitted.')
                return redirect(url)


from .models import HomePage, Ingredient, FollowGallery

def home(request):
    homepage = HomePage.objects.first()
    products = Product.objects.filter(is_available=True).order_by('-created_date')[:9]
    ingredients = Ingredient.objects.all()
    follow_images = FollowGallery.objects.all()

    context = {
        'homepage': homepage,
        'products': products,
        'ingredients': ingredients,
        'follow_images': follow_images,
    }
    return render(request, 'home.html', context)