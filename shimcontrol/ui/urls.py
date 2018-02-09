from django.conf.urls import include, url
from django.contrib import admin

from shimcontrol import api

urlpatterns = [
    url(r'^api/', include(api.urls)),
    url(r'^admin/', include(admin.site.urls)),
]