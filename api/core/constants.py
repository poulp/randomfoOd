#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

SITE_ROOT = os.path.realpath(os.path.dirname(os.path.dirname(__file__)))

RDF_XML = 'application/rdf+xml'
JSON = 'application/json'

BASE_URI = 'http://www.random-food.com/'
BASE_URI_UTENSIL = BASE_URI + 'utensil#'
BASE_URI_ACTION = BASE_URI + 'recipe#'

NAMESPACES = {
    'monnet':       'http://www.monnet-project.eu/lemon#',
    'wiki-terms':   'http://wiktionary.dbpedia.org/terms/',
    'food':         'http://data.lirmm.fr/ontologies/food#',
    'random_food':  BASE_URI + 'ontology#'
}

SPARQL_ENDPOINTS = {
    'wiktionary': 'http://wiktionary.dbpedia.org/sparql',
    'localhost': 'http://localhost:9091/sparql'
}

STORE = {
    'utensils': os.path.join(SITE_ROOT, 'core/store/utensils.rdf'),
    'actions':  os.path.join(SITE_ROOT, 'core/store/actions.rdf')
}
