from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _

from taggit.models import TagBase


class ConditionCategory(models.Model):
    name = models.CharField(max_length=150, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    class Meta:
        verbose_name = _('Condition Category')
        verbose_name_plural = _('Condition Categories')
        ordering = ['name']

    def __str__(self):
        return u'%s' % self.name

    def get_conditions(self):
        return Condition.objects.filter(category=self)


class Condition(TagBase):
    category = models.ForeignKey(ConditionCategory, null=True, blank=True, default=None, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)
    special_case = models.BooleanField(default=False, null=True, blank=True)
    image_one = models.ImageField(upload_to='static/img/conditions', null=True, blank=True)
    image_two = models.ImageField(upload_to='static/img/conditions', null=True, blank=True)
    image_three = models.ImageField(upload_to='static/img/conditions', null=True, blank=True)
    # Some conditions are known by many names
    alternate_name_one = models.CharField(max_length=150, null=True, blank=True)
    alternate_name_two = models.CharField(max_length=150, null=True, blank=True)
    alternate_name_three = models.CharField(max_length=150, null=True, blank=True)
    alternate_name_four = models.CharField(max_length=150, null=True, blank=True)
    video = models.CharField(max_length=300, null=True, blank=True)
    
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    class Meta:
        verbose_name = _('Condition')
        verbose_name_plural = _('Conditions')
        ordering = ['name']
