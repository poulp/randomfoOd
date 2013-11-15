#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import request
from flask_negotiate import produces, consumes

from rdflib import ConjunctiveGraph
from rdfalchemy.rdfSubject import rdfSubject

from generators import IngredientGenerator, RecipeGenerator
from models import Action
from sparql_constants import STORE_FILE
from . import app

PREFIX = '/api/v1'
RDF_XML = 'application/rdf+xml'


@app.route(PREFIX + '/ingredient/gen/<int:number>', methods=['GET'])
@produces('application/xml')
def get_ingredients(number):
    rdfSubject.db = ConjunctiveGraph()
    IngredientGenerator.generate(number)
    return rdfSubject.db.serialize(format=RDF_XML)


@app.route(PREFIX + '/action/add', methods=['POST'])
@consumes('application/json')
def add_action():
    rdfSubject.db = ConjunctiveGraph()
    a = Action(label=request.json['label'])
    a.db.load(STORE_FILE, format=RDF_XML)
    a.db.serialize(STORE_FILE, format=RDF_XML)
    return ''


@app.route(PREFIX + '/recipe/gen', methods=['GET'])
@produces('application/xml')
def get_recipe():
    rdfSubject.db = ConjunctiveGraph()
    RecipeGenerator.generate()
    return rdfSubject.db.serialize(format=RDF_XML)