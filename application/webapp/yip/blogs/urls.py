"""
YIP blog urls
"""


from django.urls import path
from . import views as views


urlpatterns = [
    path('list-authors/', views.ListSelectAuthors.as_view()),
    path('select-author/', views.ListSelectAuthors.as_view()),
    path('list-blog-posts/', views.ListSelectBlogPosts.as_view()),
    path('select-blog-post/', views.ListSelectBlogPosts.as_view()),
]
