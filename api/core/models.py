#!/usr/bin/env python
# -*- coding: utf-8 -*-

from rdflib import Namespace

from rdfalchemy import rdfSingle, rdfMultiple
from rdfalchemy.rdfSubject import rdfSubject

from constants import NAMESPACES


rdf = Namespace(NAMESPACES['rdf'])
food = Namespace(NAMESPACES['food'])
random_food = Namespace(NAMESPACES['random_food'])


class Ingredient(rdfSubject):
    rdf_type = food.Ingredient
    label = rdfSingle(rdf.label)
    quantity = rdfSingle(food.quantity)
    unit = rdfSingle(food.unit)


class Action(rdfSubject):
    rdf_type = random_food.Action
    label = rdfSingle(rdf.label)


class Utensil(rdfSubject):
    rdf_type = random_food.Utensil
    label = rdfSingle(rdf.label)


class Transformation(rdfSubject):
    rdf_type = random_food.Transformation
    label = rdfSingle(rdf.label)


class Recipe(rdfSubject):
    rdf_type = food.Recipe
    person_nb = rdfSingle(rdf.Literal)
    ingredients = rdfMultiple(food.Ingredient)
    utensils = rdfMultiple(random_food.Utensil)
    # transformations = rdfMultiple()
