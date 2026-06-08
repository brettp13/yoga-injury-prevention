"""
YIP faqs urls
"""


from django.urls import path
from . import views as views


urlpatterns = [
    path('list-faqs/', views.ListSelectFAQs.as_view()),
    path('select-faq/', views.ListSelectFAQs.as_view()),
]
