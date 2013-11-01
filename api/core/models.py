#!/usr/bin/env python
# -*- coding: utf-8 -*-

from rdflib import Namespace

from rdfalchemy import rdfSingle
from rdfalchemy.rdfSubject import rdfSubject

from api.core.sparql_constants import NAMESPACES


rdfs = Namespace(NAMESPACES['rdfs'])
food = Namespace(NAMESPACES['food'])


class Ingredient(rdfSubject):
    rdf_type = food.Ingredient
    label = rdfSingle(rdfs.label)
    quantity = rdfSingle(food.quantity, 0)
    unit = rdfSingle(food.unit)