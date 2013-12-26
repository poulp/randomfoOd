# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, RequestContext, redirect
from forms import AddUtensil

from utils import Recipe, get_utensils, add_utensil, \
    get_actions, get_images_from_label


def home_recette(request):
    c = {}
    return render_to_response('recette/home_recette.html', c, RequestContext(request))


def gen_recette(request):
    r = Recipe()
    if request.method == "POST":
        pass
    else:
        r.request()
    
    list_img = get_images_from_label(r.ing1.__unicode__())
    c = {
        'recipe': r,
        'list_img': list_img,
    }
    return render_to_response('recette/gen_recette.html', c, RequestContext(request))


def home_contribute(request):
    list_utensils = get_utensils()
    list_actions = get_actions()
    c = {
        "utensils": list_utensils,
        "actions": list_actions,
    }
    return render_to_response('recette/home_contribute.html', c, RequestContext(request))


def utensil_contribute(request):
    if request.method == 'POST':
        form = AddUtensil(request.POST)
        if form.is_valid():
            if add_utensil(form.cleaned_data["label"]):
                return redirect("/")
    else:
        form = AddUtensil()
    c = {
        'form': form,
    }
    return render_to_response('recette/utensil_contribute.html', c, RequestContext(request))


def add_contribute(request):
    return render_to_response('recette/add_contribute.html', {}, RequestContext(request))
