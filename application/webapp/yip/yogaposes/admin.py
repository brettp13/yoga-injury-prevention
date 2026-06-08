from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from .models import YogaPose, BeneficialPoses, WorkAroundYogaPose

class YogaPoseAdmin(SummernoteModelAdmin):
    list_display = [
        'english_name',
        'sanskrit_name',
        'created',
        'updated'
    ]
    readonly_fields = ['created']
    search_fields = ['english_name', 'sanskrit_name']
    summernote_fields = ('info',)

    class Meta:
        model = YogaPose


class BeneficialPosesAdmin(SummernoteModelAdmin):
    list_display = [
        'condition',
        'created',
        'updated'
    ]
    readonly_fields = ['created']
    search_fields = ['condition']
    summernote_fields = ['why_these_poses_help']

    class Meta:
        model = BeneficialPoses


class WorkAroundYogaPoseAdmin(SummernoteModelAdmin):
    list_display = [
        'title',
        'created',
        'updated'
    ]
    readonly_fields = ['created']
    search_fields = ['title']
    summernote_fields = ['description']

    class Meta:
        model = WorkAroundYogaPose 


admin.site.register(YogaPose, YogaPoseAdmin)
admin.site.register(BeneficialPoses, BeneficialPosesAdmin)
admin.site.register(WorkAroundYogaPose, WorkAroundYogaPoseAdmin)
