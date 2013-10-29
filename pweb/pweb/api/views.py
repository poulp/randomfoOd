from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from rdflib import Graph, RDF, BNode, Literal
from rdflib.namespace import FOAF

def index(request):
    return HttpResponse(status=501)

def get_recip(request):
    return HttpResponse(status=501)

# example qui retourne les noms de toutes les personnes
# contenu dans le fichier rdf
def get_all_person(request):
    g = Graph()
    g.load('pweb/api/rdf/pers.xml', format='xml')

    # SPARQL
    res = g.query(
    """
    SELECT ?name
    WHERE {
        ?person foaf:name ?name
    }
    """,
    initNs={ "foaf":FOAF })

    # petite negociation de contenu
    if request.META["CONTENT_TYPE"] == "application/json":
        return HttpResponse(res.serialize(format='json'),content_type="application/json")
    if request.META["CONTENT_TYPE"] == "text/xml":
        return HttpResponse(res.serialize(format='xml'),content_type="text/xml")
    return HttpResponse("Aucune Negociation de contenu")

# pour virer la vérification csrf
@csrf_exempt
def add_person(request):
    # on recupere le parametre en post
    if request.method == 'POST':
        try:
            name = request.POST.get('name','')
        except:
            return HttpResponse(status=404)

        g = Graph()
        g.load('pweb/api/rdf/pers.xml', format='xml')
        
        # nouveau noeud sans uri
        person = BNode()
        # on ajoute au graphe le triplet
        # person est du type Personne
        g.add((person,RDF.type,FOAF.Person))
        # person a pour nom "machin"
        g.add((person,FOAF.name,Literal(name)))
        g.bind("foaf",FOAF)

        # on sauve le graphe ( pour l'instant directement dans le fichier)
        g.serialize('pweb/api/rdf/pers.xml',format='xml')

        return HttpResponse(g.serialize(format='xml'),content_type="text/xml")
    return HttpResponse(status=404)
