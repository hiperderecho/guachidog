import os
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.views.generic import RedirectView

THIS_DIR = os.path.dirname(os.path.realpath(__file__))
ROOT_DIR = os.path.dirname(THIS_DIR)

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
  url(r'^robots.txt$', RedirectView.as_view(url='/static/robots.txt')),
  url(r'^', include('website.frontend.urls')),
  url(r'^admin/', include(admin.site.urls)),
]
