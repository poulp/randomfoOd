#!/usr/bin/env python
# -*- coding: utf-8 -*-

RDF_XML = 'application/rdf+xml'

BASE_URI = 'http://www.random-food.com/'
BASE_URI_UTENSIL = BASE_URI + 'utensil#'
BASE_URI_RECIPE = BASE_URI + 'recipe#'

NAMESPACES = {
    'monnet':       'http://www.monnet-project.eu/lemon#',
    'wiki-terms':   'http://wiktionary.dbpedia.org/terms/',
    'food':         'http://data.lirmm.fr/ontologies/food#',
    'random_food':  BASE_URI + 'ontology#'
}

SPARQL_ENDPOINTS = {
    'wiktionary': 'http://wiktionary.dbpedia.org/sparql'
}

STORE = {
    'utensils': 'core/store/utensils.rdf',
    'recipes':  'core/store/recipes.rdf'
}