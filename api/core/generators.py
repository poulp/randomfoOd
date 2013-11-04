#!/usr/bin/env python
# -*- coding: utf-8 -*-

from rdfalchemy.sparql import SPARQLGraph
from sparql_constants import NAMESPACES, SPARQL_ENDPOINTS


class IngredientGenerator(object):

    query = """
            SELECT DISTINCT ?label WHERE
            {
                ?x rdfs:label ?label .
                ?x monnet:sense ?sense .
                ?sense dc:language wiki-terms:French .
                ?sense wiki-terms:hasPoS wiki-terms:Noun .
                ?sense wiki-terms:hasMeaning ?meaning .

                FILTER langMatches(lang(?meaning), "FR")
                FILTER langMatches(lang(?label), "FR")
            }
            OFFSET 0 LIMIT 10
            """
    # TODO : méthode de retour (json, xml) et factoriser la connexion sparql.
    def generate(self, number):
        graph = SPARQLGraph(SPARQL_ENDPOINTS['wiktionary'])
        result = list(graph.query(self.query, resultMethod='xml', initNs=NAMESPACES))
        return [x[0].toPython() for x in result]
