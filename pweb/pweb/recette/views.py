# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, RequestContext, redirect, get_object_or_404
from forms import AddUtensil, AddAction
from django.http import HttpResponse
from django.contrib.auth.models import User

from utils import Recipe, get_utensils, add_utensil, \
    get_actions, get_images_from_label, add_action, get_actions_from_utensil, add_utensil_actions_json
import urllib2
from django.views.decorators.csrf import csrf_exempt
import models
import json

def home_recette(request):
    c = {
        "recipe" : models.Recipe.objects.all().order_by('-pk')[:3],
        "recipe_rate" : models.get_top_recipe()
    }
    return render_to_response('recette/home_recette.html', c, RequestContext(request))


def gen_recette(request):
    r = Recipe()
    if request.method == "POST":
        recipe = models.Recipe()
        recipe.title = request.POST.get("title","")
        recipe.nb_person = request.POST.get("nb","")
        recipe.user = request.user
        recipe.image = request.POST.get("image","")
        ingredients = request.POST.getlist("ing","")
        recipe.ingredients = '*'.join(ingredients)
        utensils = request.POST.getlist("utensil","")
        recipe.utensils = '*'.join(utensils)
        transformations = request.POST.getlist("transformation","")
        recipe.transformations = '*'.join(transformations)
        recipe.save()
        return redirect("/recette/")
    else:
        r.request(dev=True)

    list_img = get_images_from_label(r.ing1.__unicode__())
    c = {
        'recipe': r,
        'list_img': list_img,
    }
    return render_to_response('recette/gen_recette.html', c, RequestContext(request))

def detail_recette(request, recipe_pk):
    recipe = get_object_or_404(models.Recipe, pk=int(recipe_pk))
    image = recipe.image if recipe.image else "http://www.urti.org/images/no-image.gif" 
    is_author = False
    if request.user == recipe.user:
        is_author = True
    c = {
        "recipe" : recipe,
        "ingredients" : recipe.ingredients.split('*'),
        "utensils" : recipe.utensils.split('*'),
        "transformations" : recipe.transformations.split('*'),
        "image" : image,
        "is_author": is_author,
        "total_rate": models.get_total_rate(recipe),
    }
    return render_to_response('recette/detail_recette.html', c, RequestContext(request))

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
                return redirect("/recette/contribute")
    else:
        form = AddUtensil()
    c = {
        'form': form,
    }
    return render_to_response('recette/utensil_contribute.html', c, RequestContext(request))

def action_contribute(request):
    if request.method == 'POST':
        form = AddAction(request.POST)
        if form.is_valid():
            if add_action(form.cleaned_data["label"]):
                return redirect("/recette/contribute")
    else:
        form = AddAction()
    c = {
        'form': form,
    }
    return render_to_response('recette/action_contribute.html', c, RequestContext(request))


def add_contribute(request):
	list_utensils = get_utensils()
	list_actions = get_actions()
	c = {
		"utensils": list_utensils,
		"actions": list_actions,
	}
	return render_to_response('recette/add_contribute.html', c, RequestContext(request))

@csrf_exempt
def add_utensil_actions(request):
    if request.method == "POST":
        dataj = request.POST.get('dataj','')
        add_utensil_actions_json(dataj)
	return HttpResponse("lol")

def get_all_actions(request):
	""" retourne toutes les actions au format json """
	return HttpResponse(json.dumps(get_actions(json=True)))

def get_actions_utensil(request):
	print urllib2.unquote(request.GET['uri'])
	try:
		furi = urllib2.unquote(request.GET['uri'])
	except:
		furi = ""
	return HttpResponse(json.dumps(get_actions_from_utensil(furi)))

@csrf_exempt
def rate_recipe(request):
    total = 0
    if request.method == "POST":
        score = request.POST.get('score', '')
        user_pk = request.POST.get('user_pk', '')
        recipe_pk = request.POST.get('recipe_pk', '')

        user = User.objects.get(pk=int(user_pk))
        recipe = models.Recipe.objects.get(pk=int(recipe_pk))

        try:
            r = models.Rate.objects.get(user=user, recipe=recipe)
            r.value = int(score)
            r.save()
        except:
            r = models.Rate(value=int(score), user=user, recipe=recipe)
            r.save()
        total = models.get_total_rate(recipe)
    return HttpResponse(total)

def delete_recette(request, recipe_pk):
    r = get_object_or_404(models.Recipe, pk=int(recipe_pk))
    r.delete()
    return redirect("/recette")

