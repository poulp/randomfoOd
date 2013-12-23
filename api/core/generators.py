#!/usr/bin/env python
# -*- coding: utf-8 -*-

from random import randint, choice, sample, shuffle
from itertools import chain

from rdflib import ConjunctiveGraph, URIRef
from rdfalchemy.rdfSubject import rdfSubject
from rdfalchemy.sparql import SPARQLGraph

from constants import SPARQL_ENDPOINTS, STORE, NAMESPACES
from models import Ingredient, Recipe, Utensil, TransformedIngredient
from utils import load_rdf_file


class Endpoints(object):
    @staticmethod
    def query(endpoint, query):
        return SPARQLGraph(SPARQL_ENDPOINTS[endpoint]).query(query, initNs=NAMESPACES, resultMethod='json')


class IngredientGenerator(object):
    """
    Génère un certain nombre d'ingrédients tirés du wiktionnaire.
    """

    endpoint = 'wiktionary'
    query = """
            SELECT DISTINCT ?label WHERE
            {{
                ?x rdfs:label ?label .
                ?x monnet:sense ?sense .
                ?sense dc:language wiki-terms:French .
                ?sense wiki-terms:hasPoS wiki-terms:Noun .
                ?sense wiki-terms:hasMeaning ?meaning .

                FILTER langMatches(lang(?meaning), "FR")
                FILTER langMatches(lang(?label), "FR")
            }}
            OFFSET {offset} LIMIT {number}
            """

    @classmethod
    def generate(cls, number):
        parameters = {'offset': randint(0, 10000), 'number': number}
        raw_result = list(Endpoints.query(cls.endpoint, cls.query.format(**parameters)))

        return [Ingredient(label=r[0],
                           quantity=randint(1, 200),
                           unit=UnitGenerator.generate()) for r in raw_result]


class UnitGenerator(object):
    # TODO : extraire les unités d'une autre source, voir http://purl.obolibrary.org/obo/uo.owl
    units = ('mg', 'kg', 'poignées', 'pincées', 'litres', 'hectolitres', 'mm', 'bonnes doses', 'paquets')

    @classmethod
    def generate(cls):
        return choice(cls.units)


class UtensilGenerator(object):
    """
    Récupère quelques ustensiles de la base de données.
    """

    @classmethod
    def generate(cls, n):
        graph = ConjunctiveGraph()
        load_rdf_file(STORE['utensils'], graph)

        all_uris = set(graph.subjects())
        n = min(n, len(all_uris))
        selected_uris = sample(all_uris, n)

        # On récupère les ustensiles voulus dans le graphe
        selected_triples = chain(*map(graph.triples, ((uri, None, None) for uri in selected_uris)))
        map(rdfSubject.db.add, selected_triples)

        utensils = [Utensil(uri) for uri in selected_uris]

        # On récupère les actions de ces ustensiles
        ActionGenerator.generate(utensils)

        return utensils


class ActionGenerator(object):
    """
    Récupère les actions des ustensiles passés en paramêtre pour les ajouter au graphe.
    """

    @classmethod
    def generate(cls, utensils):
        graph = ConjunctiveGraph()
        load_rdf_file(STORE['actions'], graph)

        for utensil in utensils:
            for action in utensil.actions:
                map(rdfSubject.db.add, graph.triples((URIRef(action), None, None)))


class TransformedIngredientGenerator(object):
    """
    Génère une liste de transformations avec les ustensiles et ingrédients fournis.
    """

    @classmethod
    def generate(cls, utensils, ingredients):
        print utensils, ingredients
        transformations = []

        while len(ingredients):
            shuffle(ingredients)
            used_utensil = choice(utensils)
            used_action = choice(used_utensil.actions)

            number_of_ingredients = min(choice([1, 2]), len(ingredients))
            used_ingredients = [ingredients.pop() for _ in range(number_of_ingredients)]

            transformation = TransformedIngredient(index=len(transformations), used_utensil=used_utensil,
                                                   used_action=used_action, used_ingredients=used_ingredients)

            transformations.append(transformation)

        return transformations


class RecipeGenerator(object):
    """
    Génère une recette complète en mixant tous les autres générateurs.
    """

    @classmethod
    def generate(cls):
        n = randint(1, 1000)
        i = IngredientGenerator.generate(randint(5, 10))
        u = UtensilGenerator.generate(randint(3, 6))
        t = TransformedIngredientGenerator.generate(u, i)

        return Recipe(person_nb=n, ingredients=i, utensils=u, transformations=t)