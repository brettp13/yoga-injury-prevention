from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _


class AcknowledgedGroup(models.Model):
    title = models.CharField(max_length=50, null=True, blank=True)
    comments = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    class Meta:
        verbose_name = _('Acknowledged Group')
        verbose_name_plural = _('Acknowledged Groups')
        ordering = ['title']

    def __unicode__(self):
        return u'%s' % self.title

    def get_members(self):
        return AcknowledgedPerson.objects.filter(group=self)


class AcknowledgedPerson(models.Model):
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    group = models.ForeignKey(AcknowledgedGroup, on_delete=models.CASCADE)
    comments = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    class Meta:
        verbose_name = _('Acknowledged Person')
        verbose_name_plural = _('Acknowledged People')
        ordering = ['first_name']

    def __unicode__(self):
        return_value = '%s %s' % (self.first_name, self.last_name)
        return u'%s' % return_value
