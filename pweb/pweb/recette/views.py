from django.shortcuts import render_to_response, RequestContext
from utils import Recipe


def home(request):
    r = Recipe()
    c = {
        'recipe': r,
    }
    return render_to_response('recette/home.html', c, RequestContext(request))
