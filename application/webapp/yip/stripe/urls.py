"""
YIP stripe urls
"""


from django.urls import path
from . import views as views


urlpatterns = [
    path('create-subscriber/', views.CreateSubscriber.as_view()),
    path('webhook/', views.WebHookEvent.as_view()),
]