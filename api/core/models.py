#!/usr/bin/env python
# -*- coding: utf-8 -*-

from rdflib import Namespace

from rdfalchemy import rdfSingle, rdfMultiple, rdfSubject, RDFS

from constants import NAMESPACES

FOOD = Namespace(NAMESPACES['food'])
RANDOM_FOOD = Namespace(NAMESPACES['random_food'])


class Ingredient(rdfSubject):
    """
    Ingrédient simple : "Tomate", "Oeuf", "Moteur à explosion".
    """
    rdf_type = FOOD.Ingredient
    label = rdfSingle(RDFS.label)
    quantity = rdfSingle(FOOD.quantity)
    unit = rdfSingle(FOOD.unit)
    origin = rdfSingle(RDFS.seeAlso)


class TransformedIngredient(Ingredient):
    """
    Ingrédient obtenu par manipulation d'autres ingrédients.
    """
    rdf_type = RANDOM_FOOD.Transformation
    index = rdfSingle(RDFS.Literal)
    used_utensil = rdfSingle(RANDOM_FOOD.Utensil)
    used_action = rdfSingle(RANDOM_FOOD.Action)
    used_ingredients = rdfMultiple(RANDOM_FOOD.Ingredient)


class Action(rdfSubject):
    """
    Une action simple : "Couper", "Cuire", "Coudre".
    """
    rdf_type = RANDOM_FOOD.Action
    label = rdfSingle(RDFS.label)


class Utensil(rdfSubject):
    """
    Un ustensile : "Cuillère à café", "Couteau suisse", "M16".
    """
    rdf_type = RANDOM_FOOD.Utensil
    label = rdfSingle(RDFS.label)
    actions = rdfMultiple(RANDOM_FOOD.Action)


class Recipe(rdfSubject):
    """
    Tout ce qui permet d'afficher une recette est présent ici.
    """
    rdf_type = FOOD.Recipe
    person_nb = rdfSingle(RANDOM_FOOD.nb_person)
    ingredients = rdfMultiple(FOOD.Ingredient)
    utensils = rdfMultiple(RANDOM_FOOD.Utensil)
    transformations = rdfMultiple(RANDOM_FOOD.Transformation)