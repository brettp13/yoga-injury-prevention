from django.contrib import admin

from .models import MarketingCampaign


class MarketingCampaignAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'description',
        'cost',
        'url',
        'number_of_subscribers',
        'created',
        'updated'
    ]
    readonly_fields = ['created']
    search_fields = ['name']

    class Meta:
        model = MarketingCampaign

admin.site.register(MarketingCampaign, MarketingCampaignAdmin)