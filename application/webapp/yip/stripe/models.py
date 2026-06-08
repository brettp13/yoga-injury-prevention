from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from campaign_tracker.models import MarketingCampaign
from user_profiles.models import UserProfile


class Subscriber(models.Model):
    user_auth = models.ForeignKey(User, on_delete=models.CASCADE)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    customer_id = models.TextField(null=True, blank=True)
    valid = models.BooleanField(default=True)
    campaign = models.ForeignKey(MarketingCampaign, on_delete=models.CASCADE, related_name='subscribers', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    class Meta:
        verbose_name = _("Subscriber")
        verbose_name_plural = _("Subscribers")
        ordering = ["user_auth"]

    def __str__(self):
        return '%s' % self.user_auth