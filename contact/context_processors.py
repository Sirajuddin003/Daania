from .models import ContactPage

def contact_info(request):
    return {
        'contact_page': ContactPage.objects.first()
    }