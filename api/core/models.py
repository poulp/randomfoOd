#!/usr/bin/env python
# -*- coding: utf-8 -*-

from rdflib import Namespace

from rdfalchemy import rdfSingle, rdfMultiple
from rdfalchemy.rdfSubject import rdfSubject

from sparql_constants import NAMESPACES


rdfs = Namespace(NAMESPACES['rdfs'])
food = Namespace(NAMESPACES['food'])


class Ingredient(rdfSubject):
    rdf_type = food.Ingredient
    label = rdfSingle(rdfs.label)
    quantity = rdfSingle(food.quantity, 0)
    unit = rdfSingle(food.unit)
    img = rdfSingle(rdfs.Literal,'')
    plural = rdfSingle(rdfs.Literal,'plural')
    gender = rdfSingle(rdfs.Literal, 'gender')
    
class Action(rdfSubject):
    # rdf_type = 
    label = rdfSingle(rdfs.label)
    verb = rdfSingle(rdfs.Literal,'Action')
  
	
class Utensil(rdfSubject):
    # rdf_type =
    label = rdfSingle(rdfs.label)


class Transformation(rdfSubject):
    rdf_type = food.Ingredient # because we get a new ingredient after a transformation
    label = rdfSingle(rdfs.label)

  
class Recipe(rdfSubject):
    rdf_type = food.Recipe
    label = rdfSingle(rdfs.label)
    personNb = rdfSingle(rdfs.Literal, 1)
    ingredients = rdfMultiple(food.Ingredient)
    #utensils = rdfMultiple()
    #transformations = rdfMultiple()
