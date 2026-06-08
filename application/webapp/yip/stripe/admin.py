from django.contrib import admin
from .models import Subscriber


class SubscriberAdmin(admin.ModelAdmin):
    list_display = [
        'user_auth',
        'valid',
        'campaign',
        'created',
        'updated'
    ]
    class Meta:
        model = Subscriber

admin.site.register(Subscriber, SubscriberAdmin)
