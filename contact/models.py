from django.db import models


# ==========================================
# CONTACT FORM MESSAGES (User Submissions)
# ==========================================
class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.email}"


# ==========================================
# CONTACT PAGE SETTINGS (Singleton)
# ==========================================
class ContactPage(models.Model):
    title = models.CharField(max_length=200, default="Get in Touch")
    subtitle = models.TextField()

    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=255)

    # WhatsApp Settings
    whatsapp_number = models.CharField(
        max_length=20,
        help_text="Enter number with country code without + (Example: 919876543210)",
        blank=True,
        null=True
    )

    whatsapp_message = models.TextField(
        default="Hello Daania Beauty, I have a question about your product.",
        blank=True
    )

    is_whatsapp_enabled = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.pk and ContactPage.objects.exists():
            raise ValueError("Only one ContactPage instance allowed.")
        return super(ContactPage, self).save(*args, **kwargs)

    def __str__(self):
        return "Contact Page Settings"