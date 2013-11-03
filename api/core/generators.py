#!/usr/bin/env python
# -*- coding: utf-8 -*-

from random import randint, choice

from rdfalchemy.sparql import SPARQLGraph

from api.core.sparql_constants import NAMESPACES, SPARQL_ENDPOINTS
from api.core.models import Ingredient


class Endpoints(object):
    @staticmethod
    def query(endpoint, query):
        return SPARQLGraph(SPARQL_ENDPOINTS[endpoint]).query(query, initNs=NAMESPACES)


class IngredientGenerator(object):
    """
    Génère un certain nombre d'ingrédients tirés du wiktionnaire.
    """

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
        endpoint = 'wiktionary'

        raw_result = list(Endpoints.query(endpoint, cls.query.format(**parameters)))

        return [Ingredient(label=r[0], quantity=randint(1, 200), unit=UnitGenerator.generate()) for r in raw_result]


class UnitGenerator(object):
    # TODO : extraire les unités d'une autre source, voir http://purl.obolibrary.org/obo/uo.owl
    units = ('mg', 'kg', 'poignée', 'pincées', 'litres', 'hectolitres', 'mm', 'bonnes doses', 'paquets')

    @classmethod
    def generate(cls):
        return choice(cls.units)
