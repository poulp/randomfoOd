#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'pweb.recette.views.home_recette', name="home_recette"),
    url(r'^(?P<recipe_pk>\d+)$', 'pweb.recette.views.detail_recette', name="detail_recette"),
    url(r'^delete/(?P<recipe_pk>\d+)$', 'pweb.recette.views.delete_recette', name="delete_recette"),
    url(r'^gen$', 'pweb.recette.views.gen_recette', name="gen_recette"),
    url(r'^contribute$', 'pweb.recette.views.home_contribute', name="home_contribute"),
    url(r'^contribute/utensil$', 'pweb.recette.views.utensil_contribute', name="utensil_contribute"),
    url(r'^contribute/action$', 'pweb.recette.views.action_contribute', name="action_contribute"),
    url(r'^contribute/add$', 'pweb.recette.views.add_contribute', name="add_contribute"),
    url(r'^contribute/utensil/actions$', 'pweb.recette.views.get_actions_utensil', name="actions_utensil_contribute"),
    url(r'^contribute/getactions$', 'pweb.recette.views.get_all_actions', name="get_actions_contribute"),
)
