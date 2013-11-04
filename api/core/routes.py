#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import request, jsonify
from flask_negotiate import produces

from generators import IngredientGenerator
from core import app

prefix = '/api/v1'

@app.route(prefix + '/gen/ingredients/<int:number>', methods=['GET'])
@produces('application/json')
def get_ingredients(number):
    g = IngredientGenerator()

    a = g.generate(number)

    return jsonify({'ingredients': a})
