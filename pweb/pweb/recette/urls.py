#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'pweb.recette.views.home_recette', name="home_recette"),
    url(r'^gen$', 'pweb.recette.views.gen_recette', name="gen_recette"),
    url(r'^contribute$', 'pweb.recette.views.home_contribute', name="home_contribute"),
    url(r'^contribute/utensil$', 'pweb.recette.views.utensil_contribute', name="utensil_contribute"),
    url(r'^contribute/add$', 'pweb.recette.views.add_contribute', name="add_contribute"),
)
