from django.conf.urls import include, url
from django.contrib import admin

from shimcontrol.api.views import ADCView, DACView

urlpatterns = [
    url(r'^adc/', ADCView.as_view()),
    url(r'^dac/', DACView.as_view()),
]
