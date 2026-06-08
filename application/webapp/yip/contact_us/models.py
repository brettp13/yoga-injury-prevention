from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _


class ContactMessage(models.Model):
    """
    Store all contact messages in the db.
    """
    full_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    class Meta:
        verbose_name = _('ContactMessage')
        verbose_name_plural = _('ContactMessages')

    def __unicode__(self):
        return u'%s' % self.email
