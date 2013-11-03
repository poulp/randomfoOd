#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask_negotiate import produces

from generators import IngredientGenerator
from api.core import app

prefix = '/api/v1'


@app.route(prefix + '/ingredient/gen/<int:number>', methods=['GET'])
@produces('application/xml')
def get_ingredients(number):
    return IngredientGenerator.generate(number)[0].db.serialize(format='application/rdf+xml')

@app.route(prefix + '/action/add', methods=['POST'])
@consumes('application/json')
def add_action():
    pass