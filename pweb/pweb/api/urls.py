from django.conf.urls import patterns, url

import views

urlpatterns = patterns('',
    url(r'^$', views.index),
    url(r'^person$', views.get_all_person),
    url(r'^person/add$', views.add_person),
)
