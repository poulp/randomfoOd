from django.shortcuts import render_to_response, RequestContext

def home(request):
    c = {}
    return render_to_response('recette/home.html',c,RequestContext(request))
