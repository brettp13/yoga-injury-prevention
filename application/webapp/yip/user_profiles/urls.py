"""
YIP user profile urls
"""


from django.urls import path
from . import views as views


urlpatterns = [
    path('create-profile/', views.CreateUserProfile.as_view()),
    path('profile-detail/', views.UserProfileDetail.as_view()),
    path('create-yoga-style/', views.ListCreateYogaStyles.as_view()),
    path('list-yoga-styles/', views.ListCreateYogaStyles.as_view()),
    path('create-search-entry/', views.CreateSearchEntry.as_view()),
]
