#!/usr/bin/env python
# -*- coding: utf-8 -*-

from urllib2 import unquote
import json
from flask import request, jsonify

from rdflib import Graph, Namespace, URIRef
from rdflib.namespace import RDF

from generators import IngredientGenerator, RecipeGenerator
from models import Utensil, Action
from constants import STORE, BASE_URI_ACTION, BASE_URI_UTENSIL, JSON, RDF_XML
from utils import reset_graph, load_rdf_file, save_rdf_file, get_rdf_graph, sanitize, produces, consumes, create_uri
from . import app

PREFIX = '/api/v1'


##### INGREDIENTS
@app.route(PREFIX + '/ingredient/gen/<int:number>', methods=['GET'])
@produces(RDF_XML)
#@reset_graph
def gen_ingredients(number):
    """ Génère <number> ingrédients """
    IngredientGenerator.generate(number)
    return get_rdf_graph()


##### ACTIONS
@app.route(PREFIX + '/action/get/', methods=['GET'])
@produces(RDF_XML)
@reset_graph
def get_actions():
    """ Liste toutes les actions """
    load_rdf_file(STORE['actions'])
    return get_rdf_graph()


@app.route(PREFIX + '/action/add', methods=['POST'])
@consumes(JSON)
@produces(JSON)
@reset_graph
def add_action():
    """ Ajouter une action """
    store_file = STORE['actions']
    label = request.json['label']

    uri = create_uri(BASE_URI_ACTION + sanitize(label))

    load_rdf_file(store_file)
    Action(resUri=uri, label=label)
    save_rdf_file(store_file)

    # On retourne une chaine vide pour renvoyer un code HTTP 200
    return jsonify({'uri': uri})


##### RECIPES
@app.route(PREFIX + '/recipe/gen', methods=['GET'])
@produces(RDF_XML)
@reset_graph
def get_recipe():
    """ Génère une recette complète """
    RecipeGenerator.generate()
    return get_rdf_graph()


##### UTENSILS
@app.route(PREFIX + '/utensil/add', methods=['POST'])
@consumes(JSON)
@produces(JSON)
@reset_graph
def add_utensil():
    """ Ajouter un ustensile """
    store_file = STORE['utensils']
    label = request.json['label']
    actions = [create_uri(uri) for uri in request.json['actions']]

    uri = create_uri(BASE_URI_UTENSIL + sanitize(label))

    load_rdf_file(store_file)
    Utensil(resUri=uri, label=label, actions=actions)
    save_rdf_file(store_file)

    return jsonify({'uri': uri})

@app.route(PREFIX + '/utensil/addactions', methods=['POST'])
@consumes(JSON)
@produces(JSON)
@reset_graph
def add_utensil_actions():
    """ Ajouter des actions à un ustensile """
    NS1 = Namespace('http://www.random-food.com/ontology#')
    store_file = STORE['utensils']
    dataj = json.loads(request.data)
    
    g = Graph()
    load_rdf_file(store_file, g)
    for s, p ,o in g.triples((None, RDF.type, NS1.Utensil)):
        if s.__str__() == dataj["utensil"]:
            print s
            for a, b, c in g.triples((s, NS1.Action,None)):
                print "remove"
                g.remove((a, b, c))

            for action in dataj["actions"]:
                g.add((s, NS1.Action, URIRef(action['uri'])))
    save_rdf_file(STORE['utensils'], g) 

    return jsonify({'uri': "test"})

@app.route(PREFIX + '/utensil/get/', methods=['GET'])
@produces(RDF_XML)
@reset_graph
def get_utensils():
    """ Liste tous les ustensiles """
    load_rdf_file(STORE['utensils'])
    return get_rdf_graph()


##### ENDPOINT SPARQL
@app.route(PREFIX + '/sparql', methods=['GET'])
@produces(RDF_XML)
@reset_graph
def sparql_endpoint():
    """ Le endpoint sparql"""
    query = unquote(request.args.get('query'))

    g = Graph()

    for filename in STORE.itervalues():
        load_rdf_file(filename, g)

    return g.query(query)


##### DOCUMENTATION
@app.route(PREFIX + '/doc', methods=['GET'])
def doc():
    """ Affiche la liste des routes disponibles"""
    documentation = {}

    for rule in app.url_map.iter_rules():
        if rule.endpoint != 'static':
            func = app.view_functions[rule.endpoint]
            documentation[rule.rule] = {
                'doc': func.__doc__,
                'methods': list(rule.methods),
                'consumes': getattr(func, 'consumes', ['*/*']),
                'produces': getattr(func, 'produces', ['*/*'])
            }

    return jsonify(documentation)
