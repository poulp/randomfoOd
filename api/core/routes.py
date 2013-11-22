#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import request
from flask_negotiate import produces, consumes

from rdflib import URIRef

from generators import IngredientGenerator, RecipeGenerator
from models import Utensil, Action
from constants import STORE, BASE_URI_ACTION, BASE_URI_UTENSIL
from utils import use_graph, load_rdf_file, save_rdf_file, get_rdf_graph, sanitize
from . import app

PREFIX = '/api/v1'


##### INGREDIENTS
@app.route(PREFIX + '/ingredient/gen/<int:number>', methods=['GET'])
@produces('application/xml')
@use_graph
def get_ingredients(number):
    IngredientGenerator.generate(number)
    return get_rdf_graph()


##### ACTIONS
@app.route(PREFIX + '/action/get/', methods=['GET'])
@produces('application/xml')
@use_graph
def get_actions():
    load_rdf_file(STORE['actions'])
    return get_rdf_graph()


@app.route(PREFIX + '/action/add', methods=['POST'])
@consumes('application/json')
@use_graph
def add_action():
    store_file = STORE['actions']
    label = request.json['label']

    load_rdf_file(store_file)
    Action(resUri=URIRef(BASE_URI_ACTION + sanitize(label)), label=label)
    save_rdf_file(store_file)

    # On retourne une chaine vide pour renvoyer un code HTTP 200
    return ''


##### RECIPES
@app.route(PREFIX + '/recipe/gen', methods=['GET'])
@produces('application/xml')
@use_graph
def get_recipe():
    RecipeGenerator.generate()
    from rdfalchemy.rdfSubject import rdfSubject
    print rdfSubject.db.all_nodes()
    return get_rdf_graph()


##### UTENSILS
@app.route(PREFIX + '/utensil/add', methods=['POST'])
@consumes('application/json')
@use_graph
def add_utensil():
    store_file = STORE['utensils']
    label = request.json['label']

    load_rdf_file(store_file)
    Utensil(resUri=URIRef(BASE_URI_UTENSIL + sanitize(label)), label=label)
    save_rdf_file(store_file)

    # On retourne une chaine vide pour renvoyer un code HTTP 200
    return ''