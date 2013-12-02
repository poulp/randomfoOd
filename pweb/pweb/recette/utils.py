# -*- coding: utf-8 -*-

import urllib2
from rdflib import Graph, Namespace
from rdflib.namespace import RDF, RDFS
from random import choice
from syntax import link_title_recipe

NS1 = Namespace('http://www.random-food.com/ontology#')
LIRMM = Namespace('http://data.lirmm.fr/ontologies/food#')


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

if __name__ == "__main__":
    r = Recipe()
    print r.utensil
