#!/usr/bin/env python
# -*- coding: utf-8 -*-

from rdflib import Namespace

from rdfalchemy import rdfSingle, rdfMultiple
from rdfalchemy.rdfSubject import rdfSubject

from api.core.sparql_constants import NAMESPACES


rdf = Namespace(NAMESPACES['rdf'])
food = Namespace(NAMESPACES['food'])
manjezan = Namespace(NAMESPACES['manjezan'])


class Ingredient(rdfSubject):
    rdf_type = food.Ingredient
    label = rdfSingle(rdf.label)
    quantity = rdfSingle(food.quantity)
    unit = rdfSingle(food.unit)
    # plural = rdfSingle(food.plural)
    # gender = rdfSingle(food.gender)


class Action(rdfSubject):
    rdf_type = manjezan.Action
    label = rdfSingle(rdf.label)
    verb = rdfSingle(rdf.Literal, 'Action')


class Utensil(rdfSubject):
    rdf_type = food.Utensil
    img = rdfSingle(rdf.Literal, '')
    plural = rdfSingle(rdf.Literal, 'plural')
    gender = rdfSingle(rdf.Literal, 'gender')


class Transformation(rdfSubject):
    rdf_type = food.Ingredient  # because we get a new ingredient after a transformation
    label = rdfSingle(rdf.label)


class Recipe(rdfSubject):
    rdf_type = food.Recipe
    label = rdfSingle(rdf.label)
    personNb = rdfSingle(rdf.Literal, 1)
    ingredients = rdfMultiple(food.Ingredient)
    # utensils = rdfMultiple()
    # transformations = rdfMultiple()
