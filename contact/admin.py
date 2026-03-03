from django.contrib import admin
from .models import ContactMessage, ContactPage


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at')
    readonly_fields = ('name', 'email', 'message', 'created_at')
    ordering = ('-created_at',)


@admin.register(ContactPage)
class ContactPageAdmin(admin.ModelAdmin):
    list_display = ('title', 'email', 'phone', 'whatsapp_number', 'is_whatsapp_enabled')