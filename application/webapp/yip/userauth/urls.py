"""
YIP Auth urls
"""


from django.urls import path
from . import views as views


urlpatterns = [
    path('create-user/', views.CreateUserAuth.as_view()),
    path('cancel-account/', views.CancelAccount.as_view()),
    path('user-detail/', views.UserAuthDetail.as_view()),
    path('does-email-exist/', views.CheckEmailAvailability.as_view()),
    path('check-password/', views.CheckPassword.as_view()),
    path('forgot-password/', views.ForgotPassword.as_view()),
    path('login/', views.CustomAuthToken.as_view()),
]
