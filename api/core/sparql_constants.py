#!/usr/bin/env python
# -*- coding: utf-8 -*-

NAMESPACES = {
    'rdf':          'http://www.w3.org/2000/01/rdf-schema#',
    'monnet':       'http://www.monnet-project.eu/lemon#',
    'wiki-terms':   'http://wiktionary.dbpedia.org/terms/',
    'food':         'http://data.lirmm.fr/ontologies/food#',
    'random_food':  'http://www.random_food.com/ontology/'
}

SPARQL_ENDPOINTS = {
    'wiktionary': 'http://wiktionary.dbpedia.org/sparql'
}

STORE_FILE = 'core/store/sesame_store.rdf'