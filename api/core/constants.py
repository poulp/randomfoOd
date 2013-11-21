#!/usr/bin/env python
# -*- coding: utf-8 -*-

BASE_URI = 'http://www.random-food.com/'
BASE_URI_UTENSIL = BASE_URI + 'utensil#'
BASE_URI_RECIPE = BASE_URI + 'recipe#'

NAMESPACES = {
    'rdf':          'http://www.w3.org/2000/01/rdf-schema#',
    'monnet':       'http://www.monnet-project.eu/lemon#',
    'wiki-terms':   'http://wiktionary.dbpedia.org/terms/',
    'food':         'http://data.lirmm.fr/ontologies/food#',
    'random_food':  BASE_URI + 'ontology#'
}

SPARQL_ENDPOINTS = {
    'wiktionary': 'http://wiktionary.dbpedia.org/sparql'
}

UTENSILS_FILE = 'core/store/utensils.rdf'
RECIPES_FILE = 'core/store/recipes.rdf'

RDF_XML = 'application/rdf+xml'