#!/usr/bin/env python
# -*- coding: utf-8 -*-

from random import randint, choice, sample
from itertools import chain

from rdflib import ConjunctiveGraph
from rdfalchemy.rdfSubject import rdfSubject
from rdfalchemy.sparql import SPARQLGraph

from constants import SPARQL_ENDPOINTS, STORE, NAMESPACES
from models import Ingredient, Recipe, Utensil
from utils import load_rdf_file


class Endpoints(object):
    @staticmethod
    def query(endpoint, query):
        return SPARQLGraph(SPARQL_ENDPOINTS[endpoint]).query(query, initNs=NAMESPACES, resultMethod='json')


class IngredientGenerator(object):
    """
    Génère un certain nombre d'ingrédients tirés du wiktionnaire.
    """

    endpoint = 'wiktionary'
    query = """
            SELECT DISTINCT ?label WHERE
            {{
                ?x rdfs:label ?label .
                ?x monnet:sense ?sense .
                ?sense dc:language wiki-terms:French .
                ?sense wiki-terms:hasPoS wiki-terms:Noun .
                ?sense wiki-terms:hasMeaning ?meaning .

                FILTER langMatches(lang(?meaning), "FR")
                FILTER langMatches(lang(?label), "FR")
            }}
            OFFSET {offset} LIMIT {number}
            """

    @classmethod
    def generate(cls, number):
        parameters = {'offset': randint(0, 10000), 'number': number}
        raw_result = list(Endpoints.query(cls.endpoint, cls.query.format(**parameters)))

        return [Ingredient(label=r[0],
                           quantity=randint(1, 200),
                           unit=UnitGenerator.generate()) for r in raw_result]


class UnitGenerator(object):
    # TODO : extraire les unités d'une autre source, voir http://purl.obolibrary.org/obo/uo.owl
    units = ('mg', 'kg', 'poignées', 'pincées', 'litres', 'hectolitres', 'mm', 'bonnes doses', 'paquets')

    @classmethod
    def generate(cls):
        return choice(cls.units)


class UtensilGenerator(object):
    """
    Récupère quelques ustensiles de la base de données.
    """

    @classmethod
    def generate(cls, n):
        n = 4
        graph = ConjunctiveGraph()
        load_rdf_file(STORE['utensils'], graph)

        all_uris = set(graph.subjects())
        n %= len(all_uris)  # Pour ne pas dépasser le nombre d'ustensiles total
        selected_uris = sample(all_uris, n)

        selected_triples = chain(*map(graph.triples, ((uri, None, None) for uri in selected_uris)))
        map(rdfSubject.db.add, selected_triples)

        return [Utensil(uri) for uri in selected_uris]


class RecipeGenerator(object):
    """
    Génère une recette complète en mixant tous les autres générateurs.
    """

    @classmethod
    def generate(cls):
        n = randint(1, 1000)
        i = IngredientGenerator.generate(randint(5, 10))
        u = UtensilGenerator.generate(randint(3, 6))
        # actions
        return Recipe(person_nb=n, ingredients=i, utensils=u)