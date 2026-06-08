from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from .models import Author, BlogPost


class AuthorAdmin(admin.ModelAdmin):
    list_display = [
        'first_name',
        'last_name',
        'website',
        'posts',
        'created',
        'updated'
    ]
    read_only_field = ['created']
    search_fields = ['first_name', 'last_name']

    def posts(self, obj):
        return obj.get_articles()

    class Meta:
        model = Author


class BlogPostAdmin(SummernoteModelAdmin):
    summernote_fields = '__all__'


admin.site.register(Author, AuthorAdmin)
admin.site.register(BlogPost, BlogPostAdmin)
