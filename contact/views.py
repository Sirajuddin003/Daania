from django.shortcuts import render, redirect
from django.contrib import messages
from .models import ContactMessage, ContactPage

def contact(request):
    contact_page = ContactPage.objects.first()

    if request.method == "POST":
        ContactMessage.objects.create(
            name=request.POST['name'],
            email=request.POST['email'],
            message=request.POST['message']
        )

        messages.success(request, "Your message has been sent successfully!")
        return redirect('contact')

    context = {
        'contact_page': contact_page
    }

    return render(request, 'contact.html', context)
