# -*- coding: utf-8 -*-

import urllib2
import json

from rdflib import Graph, Namespace
from rdflib.namespace import RDF, RDFS
from random import choice
from syntax import link_title_recipe

NS1 = Namespace('http://www.random-food.com/ontology#')
LIRMM = Namespace('http://data.lirmm.fr/ontologies/food#')

ADD_UTENSIL_URL = "http://localhost:5000/api/v1/utensil/add"
GET_UTENSIL_URL = "http://localhost:5000/api/v1/utensil/get"
GET_ACTION_URL = "http://localhost:5000/api/v1/action/get"


##### OBJECTS #####

class Ingredient(object):
    def __init__(self, name, unit, quantity):
        self.name = name
        self.unit = unit
        self.quantity = quantity

    def __unicode__(self):
        return self.name


class Utensil(object):
    def __init__(self, name):
        self.name = name

    def __unicode__(self):
        return self.name

class Action(object):
    def __init__(self, name):
        self.name = name

    def __unicode__(self):
        return self.name

class Recipe(object):
    def __init__(self):
        self.url = "http://localhost:5000/api/v1/recipe/gen"
        self.graph = Graph()

        self.ingredient = []
        self.utensil = []
        self.nb_pers = 0

        self.request()

    def request(self):
        headers = {"Accept": "application/xml"}
        req = urllib2.Request(self.url, headers=headers)
        response = urllib2.urlopen(req)

        self.graph.parse(data=response.read(), format="xml")

        #ingredients
        for s, p, o in self.graph.triples((None, RDF.type, LIRMM.Ingredient)):
            self.ingredient.append(Ingredient(self.graph.value(s, RDFS.label), self.graph.value(s, LIRMM.unit), self.graph.value(s, LIRMM.quantity)))

        #utensil
        for s, p, o in self.graph.triples((None, RDF.type, NS1.Utensil)):
            self.utensil.append(Utensil(self.graph.value(s, RDFS.label)))

    def get_title(self):
        ing1 = choice(self.ingredient)
        ing2 = choice(self.ingredient)

        return link_title_recipe(ing1.__unicode__(), ing2.__unicode__())


##### Utils function #####
def get_utensils():
    """ Return a list who contains all the Utensil objects """
    headers = {"Accept": "application/xml"}
    req = urllib2.Request(GET_UTENSIL_URL, headers=headers)
    response = urllib2.urlopen(req)
    graph = Graph()
    graph.parse(data=response.read(), format="xml")
    list_utensils = []

    for s, p, o in graph.triples((None, RDF.type, NS1.Utensil)):
        list_utensils.append(Utensil(graph.value(s, RDFS.label)))
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
    headers = {"Accept": "application/xml"}
    req = urllib2.Request(GET_ACTION_URL, headers=headers)
    response = urllib2.urlopen(req)
    graph = Graph()
    graph.parse(data=response.read(), format="xml")
    list_actions = []

    for s, p, o in graph.triples((None, RDF.type, NS1.Action)):
        list_actions.append(Action(graph.value(s, RDFS.label)))
    return list_actions

if __name__ == "__main__":
    r = Recipe()
    print r.utensil
