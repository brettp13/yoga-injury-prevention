from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _

from .state_choices import STATE_CHOICES as SC


class UserProfile(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    country = models.CharField(max_length=5, null=True, blank=True)
    region = models.CharField(max_length=50, null=True, blank=True)
    street = models.CharField(max_length=250, null=True, blank=True)
    city = models.CharField(max_length=30, null=True, blank=True)
    state = models.CharField(max_length=2, choices=SC, null=True, blank=True, default='!!')
    postal_code = models.CharField(max_length=12, null=True, blank=True)
    yoga_style = models.ForeignKey('YogaStyle', on_delete=models.CASCADE, null=True)
    is_teacher = models.NullBooleanField(null=True, blank=True)
    number_of_logins = models.IntegerField(null=True, blank=True, default=0)
    number_of_queries = models.IntegerField(null=True, blank=True, default=0)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    class Meta:
        verbose_name = _("User Profile")
        verbose_name_plural = _("User Profiles")
        ordering = ["user"]

    def __str__(self):
        return_value = '%s %s' % (self.first_name, self.last_name)
        return u'%s' % return_value


class YogaStyle(models.Model):
    title = models.CharField(max_length=50, default='No title')
    public = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    class Meta:
        verbose_name = _("Yoga Style")
        verbose_name_plural = _("Yoga Styles")
        ordering = ["title"]

    def __str__(self):
        return u"%s" % self.title


class SearchEntry(models.Model):
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    search_criteria = models.TextField(null=True, blank=True)
    search_type = models.CharField(max_length=20, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    class Meta:
        verbose_name = _("Search History")
        verbose_name_plural = _("Search History")

    def __str__(self):
        return u"%s  %s  %s" % (self.created, self.profile, self.search_criteria)
