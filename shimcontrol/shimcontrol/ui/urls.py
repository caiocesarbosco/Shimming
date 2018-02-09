from django.conf.urls import include, url
from django.contrib import admin

import shimcontrol.api.urls

urlpatterns = [
    url(r'^api/', include(shimcontrol.api.urls)),
    url(r'^admin/', include(admin.site.urls)),
]
