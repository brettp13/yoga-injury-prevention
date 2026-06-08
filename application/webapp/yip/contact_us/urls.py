"""
YIP contact page urls
"""


from django.urls import path
from . import views as views


urlpatterns = [
    path('', views.CreateContactMessage.as_view()),
]