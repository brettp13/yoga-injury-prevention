from django.db import models
from django.utils.translation import ugettext_lazy as _


class MarketingCampaign(models.Model):
    name = models.CharField(max_length=150, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    cost = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    url = models.CharField(max_length=100, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return '%s' % self.name

    def number_of_subscribers(self):
        return self.subscribers.all().count()

    class Meta:
        verbose_name = _('Marketing Campaign')
        verbose_name_plural = _('Marketing Campaigns')
        ordering = ['created']

