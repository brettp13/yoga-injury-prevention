"""
Base YIP url configuration
"""


from django.contrib import admin
from django.conf.urls import handler404
from django.urls import include, path

from campaign_tracker.views import from_iayt
from homepage.views import homepage


handler404 = homepage

urlpatterns = [
    # Campaign urls
    path('iayt/', from_iayt),

    # Application urls
    path('admin/', admin.site.urls),
    path('auth/', include('userauth.urls')),
    path('profile/', include('user_profiles.urls')),
    path('yoga-poses/', include('yogaposes.urls')),
    path('conditions/', include('conditions.urls')),
    path('faqs/', include('faqs.urls')),
    path('summernote/', include('django_summernote.urls')),
    path('blog/', include('blogs.urls')),
    path('acknowledgements/', include('acknowledgements.urls')),
    path('search-by-pose/', include('search_by_pose.urls')),
    path('search-by-conditions/', include('search_by_condition.urls')),
    path('contact-us/', include('contact_us.urls')),
    path('stripe/', include('stripe.urls')),
    path('campaigns/', include('campaign_tracker.urls')),
    path('', homepage),
]

admin.site.site_title = "Yoga Injury Prevention Administration"
