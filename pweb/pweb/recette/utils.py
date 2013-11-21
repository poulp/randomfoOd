import urllib2
from rdflib import Graph, Namespace
from rdflib.namespace import RDF, RDFS


NS1 = Namespace('http://www.random-food.com/')
LIRMM = Namespace('http://data.lirmm.fr/ontologies/food#')

class Recipe:
    def __init__(self):
        self.url = "http://localhost:5000/api/v1/recipe/gen"
        self.graph = Graph()
        self.request()

    def request(self):
        headers = {"Accept": "application/xml"}
        req = urllib2.Request(self.url, headers=headers)
        response = urllib2.urlopen(req)

        self.graph.parse(data=response.read(), format="xml")

        for s,p,o in self.graph.triples((None, RDF.type, LIRMM.Ingredient)):
            self.graph.preferredLabel(s)

if __name__ == "__main__":
    r = Recipe()
