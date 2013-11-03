#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import request
from flask_negotiate import produces, consumes
from rdflib import Graph
from rdflib.term import URIRef

from api.core.generators import IngredientGenerator
from api.core.models import Action
from api.core.sparql_constants import STORE_FILE
from api.core import app

prefix = '/api/v1'
rdf_xml = 'application/rdf+xml'


@app.route(prefix + '/ingredient/gen/<int:number>', methods=['GET'])
@produces('application/xml')
def get_ingredients(number):
    return IngredientGenerator.generate(number)[0].db.serialize(format=rdf_xml)


@app.route(prefix + '/action/add', methods=['POST'])
@consumes('application/json')
def add_action():
    a = Action(label=request.json['label'])
    a.db.load(STORE_FILE, format=rdf_xml)
    a.db.serialize(STORE_FILE, format=rdf_xml)

    return ''