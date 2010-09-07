# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url
from pages.redsolution_setup.admin import PagesSettingsAdmin
admin_instance = PagesSettingsAdmin()

urlpatterns = patterns('',
    url(r'^$', admin_instance.change_view, name='pages_index'),
)
