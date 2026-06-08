from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _


class Author(models.Model):
    first_name = models.CharField(max_length=20, null=True, blank=True)
    last_name = models.CharField(max_length=28, null=True, blank=True)
    website = models.CharField(max_length=100, null=True, blank=True)
    twitter = models.CharField(max_length=100, null=True, blank=True)
    facebook = models.CharField(max_length=100, null=True, blank=True)
    instagram = models.CharField(max_length=100, null=True, blank=True)
    picture = models.ImageField(upload_to="static/img/authors", null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    class Meta:
        verbose_name = _('Blog Author')
        verbose_name_plural = _('Blog Authors')
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return u'%s %s' % (self.first_name, self.last_name)

    def author_name(self):
        return u'%s %s' % (self.first_name, self.last_name)

    def get_articles(self):
        return BlogPost.objects.filter(author=self)


class BlogPost(models.Model):
    title = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField(upload_to="static/img/blog_posts", null=True, blank=True)
    body = models.TextField(null=True, blank=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    class Meta:
        verbose_name = _('Blog Post')
        verbose_name_plural = _('Blog Posts')
        ordering = ['title']

    def __str__(self):
        return u'%s' % self.title

    def get_author_image(self):
        return self.author.picture
