from django.shortcuts import render_to_response, RequestContext, redirect
import urllib2
import json
from forms import AddUtensil
from utils import Recipe


ADD_UTENSIL_URL = "http://localhost:5000/api/v1/utensil/add"


def home(request):
    r = Recipe()
    c = {
        'recipe': r,
    }
    return render_to_response('recette/home.html', c, RequestContext(request))


def home_contribute(request):
    c = {}
    return render_to_response('recette/home_contribute.html', c, RequestContext(request))


def utensil_contribute(request):
    if request.method == 'POST':
        form = AddUtensil(request.POST)
        if form.is_valid():
            params = {
                'label': form.cleaned_data['label'],
            }
            data = json.dumps(params)
            headers = {"Content-Type": "application/json"}
            req = urllib2.Request(ADD_UTENSIL_URL, data, headers)
            urllib2.urlopen(req)
            return redirect("/")
    else:
        form = AddUtensil()
    c = {
        'form': form,
    }
    return render_to_response('recette/utensil_contribute.html', c, RequestContext(request))
