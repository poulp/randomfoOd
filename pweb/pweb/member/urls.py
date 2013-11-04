#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

import views
import forms

urlpatterns = patterns('',
    url(r'^login$', 'django.contrib.auth.views.login', {'template_name':'member/login.html', 'authentication_form': forms.LoginForm}),
    url(r'^logout$', 'django.contrib.auth.views.logout_then_login'),
)
