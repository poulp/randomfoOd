#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import request
from flask_negotiate import produces, consumes

from rdflib import ConjunctiveGraph, URIRef
from rdfalchemy.rdfSubject import rdfSubject

from generators import IngredientGenerator, RecipeGenerator
from models import Utensil

import constants
import utils

from . import app

PREFIX = '/api/v1'

@app.route(PREFIX + '/ingredient/gen/<int:number>', methods=['GET'])
@produces('application/xml')
def get_ingredients(number):
    rdfSubject.db = ConjunctiveGraph()
    IngredientGenerator.generate(number)
    return rdfSubject.db.serialize(format=constants.RDF_XML)


@app.route(PREFIX + '/recipe/gen', methods=['GET'])
@produces('application/xml')
def get_recipe():
    rdfSubject.db = ConjunctiveGraph()
    RecipeGenerator.generate()
    return rdfSubject.db.serialize(format=constants.RDF_XML)


@app.route(PREFIX + '/utensil/add', methods=['POST'])
@consumes('application/json')
def add_utensil():
    rdfSubject.db = ConjunctiveGraph()
    utils.load_rdf_file(constants.UTENSILS_FILE)

    # On ajoute l'ustensile dans le graphe par effet de bord
    label = request.json['label']
    Utensil(resUri=URIRef(constants.BASE_URI_UTENSIL + utils.sanitize(label)),
            label=label)

    # On sauvegarde
    rdfSubject.db.serialize(constants.UTENSILS_FILE, format=constants.RDF_XML)

    # On retourne une chaine vide pour renvoyer un code 200
    return ''