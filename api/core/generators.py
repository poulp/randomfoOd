#!/usr/bin/env python
# -*- coding: utf-8 -*-

from random import randint

from rdfalchemy.sparql import SPARQLGraph

from api.core.sparql_constants import NAMESPACES, SPARQL_ENDPOINTS
from api.core.models import Ingredient


class Endpoints(object):
    wiktionary = SPARQLGraph(SPARQL_ENDPOINTS['wiktionary'])

    @staticmethod
    def query(endpoint, query):
        return endpoint.query(query, initNs=NAMESPACES)


class IngredientGenerator(object):

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
        """
        Génère un certain nombre d'ingrédients tirés du wiktionnaire.
        """

        parameters = {'offset': randint(0, 10000), 'number': number}
        endpoint = Endpoints.wiktionary

        raw_result = list(Endpoints.query(endpoint, cls.query.format(**parameters)))

        return [Ingredient(label=r[0]) for r in raw_result]