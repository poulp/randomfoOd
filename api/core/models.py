#!/usr/bin/env python
# -*- coding: utf-8 -*-

from rdflib import Namespace

from rdfalchemy import rdfSingle, rdfMultiple
from rdfalchemy import rdfSubject, RDFS

from constants import NAMESPACES

FOOD = Namespace(NAMESPACES['food'])
RANDOM_FOOD = Namespace(NAMESPACES['random_food'])


class Ingredient(rdfSubject):
    rdf_type = FOOD.Ingredient
    label = rdfSingle(RDFS.label)
    quantity = rdfSingle(FOOD.quantity)
    unit = rdfSingle(FOOD.unit)


class Action(rdfSubject):
    rdf_type = RANDOM_FOOD.Action
    label = rdfSingle(RDFS.label)


class Utensil(rdfSubject):
    rdf_type = RANDOM_FOOD.Utensil
    label = rdfSingle(RDFS.label)
    actions = rdfMultiple(RANDOM_FOOD.Action)


class Recipe(rdfSubject):
    rdf_type = FOOD.Recipe
    person_nb = rdfSingle(RANDOM_FOOD.nb_person)
    ingredients = rdfMultiple(FOOD.Ingredient)
    utensils = rdfMultiple(RANDOM_FOOD.Utensil)