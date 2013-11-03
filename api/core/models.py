#!/usr/bin/env python
# -*- coding: utf-8 -*-

from rdflib import Namespace

from rdfalchemy import rdfSingle, rdfMultiple
from rdfalchemy.rdfSubject import rdfSubject

from api.core.sparql_constants import NAMESPACES


rdfs = Namespace(NAMESPACES['rdfs'])
food = Namespace(NAMESPACES['food'])
manjezan = Namespace(NAMESPACES['manjezan'])


class Ingredient(rdfSubject):
    rdf_type = food.Ingredient
    label = rdfSingle(rdfs.label)
    quantity = rdfSingle(food.quantity, 0)
    unit = rdfSingle(food.unit)
    # plural = rdfSingle(food.plural)
    # gender = rdfSingle(food.gender)


class Action(rdfSubject):
    rdf_type = manjezan.Action
    label = rdfSingle(rdfs.label)
    verb = rdfSingle(food.verb)


class Utensil(rdfSubject):
    rdf_type = food.Utensil
    label = rdfSingle(rdfs.label)


class Transformation(rdfSubject):
    rdf_type = food.Transformation
    label = rdfSingle(rdfs.label)


class Recipe(rdfSubject):
    rdf_type = food.Recipe
    label = rdfSingle(rdfs.label)
    personNb = rdfSingle(rdfs.Literal, 1)
    ingredients = rdfMultiple(food.Ingredient)
    utensils = rdfMultiple(food.Utensil)
    transformations = rdfMultiple(food.Transformation)