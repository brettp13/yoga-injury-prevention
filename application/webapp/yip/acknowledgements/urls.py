"""
YIP acknowledgement urls
"""


from django.urls import path
from . import views as views


urlpatterns = [
    path('list-acknowledged-groups/', views.ListAcknowledgedGroups.as_view()),
    path('list-acknowledged-people/', views.ListSelectAcknowledgedPerson.as_view()),
    path('select-acknowledged-person/', views.ListSelectAcknowledgedPerson.as_view()),
]
