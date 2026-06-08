"""
YIP Search by condition urls
"""

from django.urls import path
from . import views as views


urlpatterns = [
    path('get-contraindicated-poses/', views.SearchForContraindicatedPoses.as_view()),
    path('get-indicated-poses/', views.SearchForIndicatedPoses.as_view()),
    path('get-beneficial-poses/', views.SearchForBeneficialPoses.as_view()),
    path('get-safe-poses/', views.SearchForSafePoses.as_view()),
    path('how-yoga-can-help/', views.WhyYogaHelps.as_view()),
]
