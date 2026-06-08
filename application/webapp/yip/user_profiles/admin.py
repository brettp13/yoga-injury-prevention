from django.contrib import admin

from .models import YogaStyle, UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    list_display = [
        'first_name',
        'last_name',
        'user',
        'is_teacher',
        'created',
        'updated'
    ]
    readonly_fields = ['created']
    search_fields = ['first_name', 'last_name']

    class Meta:
        model = UserProfile

admin.site.register(YogaStyle)
admin.site.register(UserProfile, UserProfileAdmin)
