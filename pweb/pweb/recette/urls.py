#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'pweb.recette.views.home', name="home_recette"),
    url(r'^contribute$', 'pweb.recette.views.home_contribute', name="home_contribute"),
    url(r'^contribute/utensil$', 'pweb.recette.views.utensil_contribute', name="utensil_contribute"),
)
