from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from .models import Condition, ConditionCategory


class ConditionAdmin(SummernoteModelAdmin):
    summernote_fields = 'description'


admin.site.register(Condition, ConditionAdmin)
admin.site.register(ConditionCategory)
