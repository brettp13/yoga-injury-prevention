from django.contrib import admin

from .models import ContactMessage


class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['email', 'full_name', 'created']
    ordering = ['created',]


admin.site.register(ContactMessage, ContactMessageAdmin)