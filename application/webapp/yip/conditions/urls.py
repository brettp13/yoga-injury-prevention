"""
YIP condition urls
"""


from django.urls import path
from . import views as views


urlpatterns = [
    path('list-conditions/', views.ListSelectConditions.as_view()),
    path('select-condition/', views.ListSelectConditions.as_view()),
    path('list-condition-categories/', views.ListSelectConditionCategory.as_view()),
    path('select-condition-category/', views.ListSelectConditionCategory.as_view()),
]
