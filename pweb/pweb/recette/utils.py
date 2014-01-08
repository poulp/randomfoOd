# -*- coding: utf-8 -*-

import urllib2
import json

from rdflib import Graph, Namespace
from rdflib.namespace import RDF, RDFS
from random import choice
from syntax import link_title_recipe

from rdfalchemy.sparql import SPARQLGraph

NS1 = Namespace('http://www.random-food.com/ontology#')
LIRMM = Namespace('http://data.lirmm.fr/ontologies/food#')

ADD_UTENSIL_URL = "http://localhost:5000/api/v1/utensil/add"
GET_UTENSIL_URL = "http://localhost:5000/api/v1/utensil/get"
GET_ACTION_URL = "http://localhost:5000/api/v1/action/get"


class Base(object):
    def __init__(self, uri):
        self.uri = uri

##### OBJECTS #####


class Ingredient(Base):
    def __init__(self, uri, name, unit, quantity):
        super(Ingredient, self).__init__(uri)
        self.name = name
        self.unit = unit
        self.quantity = quantity

    def __unicode__(self):
        return self.name


class Utensil(Base):
    def __init__(self, uri, name):
        super(Utensil, self).__init__(uri)
        self.name = name

    def __unicode__(self):
        return self.name


class Action(object):
    def __init__(self, name):
        self.name = name

    def __unicode__(self):
        return self.name


class Transformation(object):
    def __init__(self, name, position, utensil, ing):
        self.name = name
        self.position = position
        self.utensil = utensil
        self.ing = ing

    def __unicode__(self):
        tmp = u""
        tmp += self.name + u" le "

        for i, n in enumerate(self.ing):
            if i == len(self.ing) - 1:
                tmp += n
            else:
                tmp += n + u" et le "

        tmp += u" à l'aide de la " + self.utensil.lower()
        return tmp


class Recipe(object):
    def __init__(self):
        self.url = "http://localhost:5000/api/v1/recipe/gen"
        self.graph = Graph()

        self.ingredient = []
        self.utensil = []
        self.nb_person = 0
        self.transformation = []

        self.ing1 = ""
        self.ing2 = ""

        self.data = ""

    def request(self, dev=False):

        if not dev:
            headers = {"Accept": "application/rdf+xml"}
            req = urllib2.Request(self.url, headers=headers)
            response = urllib2.urlopen(req)
            self.data = response.read()
            self.graph.parse(data=self.data, format="xml")
        else:
            #self.graph.parse(data="dev_rdf.xml", format="xml")
            self.graph.load("pweb/recette/dev_rdf.xml", format="xml")

        #ingredients
        for s, p, o in self.graph.triples((None, RDF.type, LIRMM.Ingredient)):
            self.ingredient.append(Ingredient(s, self.graph.value(s, RDFS.label), self.graph.value(s, LIRMM.unit), self.graph.value(s, LIRMM.quantity)))

        #utensil
        for s, p, o in self.graph.triples((None, RDF.type, NS1.Utensil)):
            self.utensil.append(Utensil(s, self.graph.value(s, RDFS.label)))

        for s, p, o in self.graph.triples((None, RDF.type, LIRMM.Recipe)):
            # nombre de personne
            self.nb_person = self.graph.value(s, NS1.nb_person)
            # transformations d'une recette
            for a, b, c in self.graph.triples((s, NS1.Transformation, None)):
                tname = self.graph.value(c, NS1.Action)
                tname = self.graph.value(tname, RDFS.label)

                tposition = self.graph.value(c, RDFS.Literal)
                tutensil = self.graph.value(self.graph.value(c, NS1.Utensil), RDFS.label)

                ing = []
                for t, y, u in self.graph.triples((c, NS1.Ingredient, None)):
                    ing.append(self.graph.value(u, RDFS.label))

                self.transformation.append(Transformation(tname,tposition,tutensil,ing))

        #reorder transfo by position
        self.transformation.sort(key=lambda x: x.position, reverse=False)

        self.ing1 = choice(self.ingredient)
        self.ing2 = choice(self.ingredient)

    def get_title(self):
        return link_title_recipe(self.ing1.__unicode__(), self.ing2.__unicode__())


##### Utils function #####
def get_utensils():
    """ Return a list who contains all the Utensil objects """
    headers = {"Accept": "application/rdf+xml"}
    req = urllib2.Request(GET_UTENSIL_URL, headers=headers)
    response = urllib2.urlopen(req)
    graph = Graph()
    graph.parse(data=response.read(), format="xml")
    list_utensils = []

    for s, p, o in graph.triples((None, RDF.type, NS1.Utensil)):
        list_utensils.append(Utensil(s, graph.value(s, RDFS.label)))
    return list_utensils


def add_utensil(label):
    """ Add utensil to the store """
    if label == "":
        return False
    params = {
        'label': label,
    }
    data = json.dumps(params)
    headers = {"Content-Type": "application/json"}
    req = urllib2.Request(ADD_UTENSIL_URL, data, headers)
    urllib2.urlopen(req)

    return True


def get_actions():
    """ Return a list who contains all the Action objects """
    headers = {"Accept": "application/rdf+xml"}
    req = urllib2.Request(GET_ACTION_URL, headers=headers)
    response = urllib2.urlopen(req)
    graph = Graph()
    graph.parse(data=response.read(), format="xml")
    list_actions = []

    for s, p, o in graph.triples((None, RDF.type, NS1.Action)):
        list_actions.append(Action(graph.value(s, RDFS.label)))
    return list_actions


def get_images_from_label(label, limit=100):
    """ return a list of url's image found by
        a label query on dbpedia
    """
    url = "http://dbpedia.org/sparql"
    query = """
            PREFIX foaf: <http://xmlns.com/foaf/0.1/>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX dbpedia-owl: <http://dbpedia.org/ontology/>
            SELECT ?img
            {
                ?uri rdfs:label ?txt.
                ?txt bif:contains "%s".
                ?uri foaf:depiction ?img.
                MINUS { ?uri rdf:type dbpedia-owl:Person . }

            } LIMIT %d
            """ % (label, limit)
    g = SPARQLGraph(url)
    result = list(g.query(query, resultMethod="json"))

    return [img_url[0].toPython() for img_url in result]
    #return []

if __name__ == "__main__":
    r = Recipe()
    print r.utensil
