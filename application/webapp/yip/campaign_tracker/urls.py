"""
YIP marketing campaign urls
"""


from django.urls import path
from . import views as views


urlpatterns = [
    path('alex/', views.from_alex),
]