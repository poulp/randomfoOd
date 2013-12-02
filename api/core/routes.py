#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import request, jsonify
from flask_negotiate import produces, consumes

from rdflib import URIRef

from generators import IngredientGenerator, RecipeGenerator
from models import Utensil, Action
from constants import STORE, BASE_URI_ACTION, BASE_URI_UTENSIL, JSON, XML
from utils import use_graph, load_rdf_file, save_rdf_file,\
    get_rdf_graph, sanitize
from . import app

PREFIX = '/api/v1'


##### INGREDIENTS
@app.route(PREFIX + '/ingredient/gen/<int:number>', methods=['GET'])
@produces(XML)
@use_graph
def get_ingredients(number):
    """ Génère <number> ingrédients """
    IngredientGenerator.generate(number)
    return get_rdf_graph()


##### ACTIONS
@app.route(PREFIX + '/action/get/', methods=['GET'])
@produces(XML)
@use_graph
def get_actions():
    """ Liste toutes les actions """
    load_rdf_file(STORE['actions'])
    return get_rdf_graph()


@app.route(PREFIX + '/action/add', methods=['POST'])
@consumes(JSON)
@use_graph
def add_action():
    """ Ajoute une action à la base de données """
    store_file = STORE['actions']
    label = request.json['label']

    load_rdf_file(store_file)
    Action(resUri=URIRef(BASE_URI_ACTION + sanitize(label)), label=label)
    save_rdf_file(store_file)

    # On retourne une chaine vide pour renvoyer un code HTTP 200
    return ''


##### RECIPES
@app.route(PREFIX + '/recipe/gen', methods=['GET'])
@produces(XML)
@use_graph
def get_recipe():
    """ Génère une recette complète """
    RecipeGenerator.generate()
    from rdfalchemy.rdfSubject import rdfSubject
    print rdfSubject.db.all_nodes()
    return get_rdf_graph()


##### UTENSILS
@app.route(PREFIX + '/utensil/add', methods=['POST'])
@consumes(JSON)
@use_graph
def add_utensil():
    """ Ajouter un ustensile """
    store_file = STORE['utensils']
    label = request.json['label']

    load_rdf_file(store_file)
    Utensil(resUri=URIRef(BASE_URI_UTENSIL + sanitize(label)), label=label)
    save_rdf_file(store_file)

    # On retourne une chaine vide pour renvoyer un code HTTP 200
    return ''


##### DOCUMENTATION
@app.route(PREFIX + '/doc', methods=['GET'])
def doc():
    """ Affiche la liste des routes disponibles"""
    func_list = {}
    for rule in app.url_map.iter_rules():
        if rule.endpoint != 'static':
            func_list[rule.rule] = [
                app.view_functions[rule.endpoint].__doc__,
                ', '.join(rule.methods)
            ]
    return jsonify(func_list)
