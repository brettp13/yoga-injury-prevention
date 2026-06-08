"""
YIP yogapose urls
"""


from django.urls import path
from . import views as views


urlpatterns = [
    path('list-poses/', views.ListSelectPoses.as_view()),
    path('select-pose/', views.ListSelectPoses.as_view()),
    path('get-workaround/', views.Workarounds.as_view()),
]
