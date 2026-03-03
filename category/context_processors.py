from .models import Category

def menu_links(request):
    return {
        'categories': Category.objects.all()
    }
