"""
YIP Search by yoga pose urls
"""

from django.urls import path
from . import views as views


urlpatterns = [
    path('search-by-pose/', views.SearchByPose.as_view()),
    path('get-conditions-helped-by-pose/', views.GetConditionsHelpedByPose.as_view()),
    path('get-conditions-contraindicated-by-pose/', views.GetConditionsContraindicatedByPose.as_view())
]
