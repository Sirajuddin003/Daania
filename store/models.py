from django.db import models
from django.urls import reverse
from decimal import Decimal
from accounts.models import Account
from django.db.models import Avg, Count
from category.models import Category

# Create your models here.

class Product(models.Model):
    product_name    = models.CharField(max_length=200)
    slug            = models.SlugField(max_length=200)
    description     = models.TextField(max_length=500, blank=True)
    price           = models.IntegerField()
    discount_percent = models.PositiveIntegerField(default=0)  # NEW FIELD
    images          = models.ImageField(upload_to='store/products')
    stock           = models.PositiveIntegerField(default=0)
    is_available    = models.BooleanField(default=True)
    category        = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date    = models.DateTimeField(auto_now_add=True)
    modified_date   = models.DateTimeField(auto_now=True)

    def get_discount_amount(self):
        if self.discount_percent > 0:
            return (self.price * self.discount_percent) / 100
        return 0

    def get_final_price(self):
        if self.discount_percent > 0:
            return int(self.price - self.get_discount_amount())
        return self.price

    def get_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug])

    def __str__(self):
        return self.product_name

    def averageReview(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(average=Avg('rating'))
        avg = 0
        if reviews['average'] is not None:
            avg = float(reviews['average'])
        return avg

    def countReview(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(count=Count('id'))
        count = 0
        if reviews['count'] is not None:
            count = int(reviews['count'])
        return count

class VariationManager(models.Manager):
    def colors(self):
        return super(VariationManager, self).filter(variation_category='color', is_active=True)

    def sizes(self):
        return super(VariationManager, self).filter(variation_category='size', is_active=True)

variation_category_choice = (
    ('color', 'color'),
    ('size', 'size'),
)

class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_category = models.CharField(max_length=100, choices=variation_category_choice)
    variation_value     = models.CharField(max_length=100)
    is_active           = models.BooleanField(default=True)
    created_date        = models.DateTimeField(auto_now=True)

    objects = VariationManager()

    def __str__(self):
        return self.variation_value


class ReviewRating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100, blank=True)
    review = models.TextField(max_length=500, blank=True)
    rating = models.FloatField()
    ip = models.CharField(max_length=20, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject


class ProductGallery(models.Model):
    product = models.ForeignKey(Product, default=None, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='store/products', max_length=255)

    def __str__(self):
        return self.product.product_name

    class Meta:
        verbose_name = 'productgallery'
        verbose_name_plural = 'product gallery'


# ==========================================
# HOMEPAGE MAIN CONTENT
# ==========================================

class HomePage(models.Model):
    # HERO SECTION
    hero_title = models.CharField(max_length=200)
    hero_description = models.TextField()
    hero_image = models.ImageField(upload_to='homepage/')
    hero_mini_image = models.ImageField(upload_to='homepage/')

    # PRODUCTS SECTION
    products_title = models.CharField(max_length=200)
    products_subtitle = models.TextField()

    # INGREDIENT SECTION TITLE
    ingredients_title = models.CharField(max_length=200)
    ingredients_subtitle = models.TextField()

    # FEATURE SECTION
    feature_title = models.TextField()
    feature_discount_text = models.CharField(max_length=50)
    feature_image = models.ImageField(upload_to='homepage/')
    feature_description = models.TextField()

    # INGREDIENT HERO SECTION
    ingredient_hero_title = models.CharField(max_length=200)
    ingredient_hero_description = models.TextField()
    ingredient_hero_image = models.ImageField(upload_to='homepage/')
    stat_customers = models.CharField(max_length=20)
    stat_products = models.CharField(max_length=20)

    # FOLLOW SECTION
    follow_title = models.CharField(max_length=200)

    def __str__(self):
        return "Homepage Content"
    


# ==========================================
# INGREDIENT MODEL
# ==========================================

class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='homepage/ingredients/')

    def __str__(self):
        return self.name
    

# ==========================================
# FOLLOW GALLERY
# ==========================================

class FollowGallery(models.Model):
    image = models.ImageField(upload_to='homepage/follow/')

    def __str__(self):
        return f"Follow Image {self.id}"
    

# ==========================================
# ABOUT PAGE MODEL
# ==========================================

class AboutPage(models.Model):
    title = models.CharField(max_length=200)
    paragraph_1 = models.TextField()
    paragraph_2 = models.TextField()
    paragraph_3 = models.TextField()
    button_text = models.CharField(max_length=100, default="Explore Our Products")
    hero_image = models.ImageField(upload_to='about/', blank=True, null=True)

    def __str__(self):
        return "About Page Content"


