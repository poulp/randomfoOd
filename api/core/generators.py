#!/usr/bin/env python
# -*- coding: utf-8 -*-

from random import randint, choice, sample, shuffle
from itertools import chain

from rdflib import ConjunctiveGraph
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
    origin = u'http://wiktionary.org/wiki/{word}'
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
    endpoint2 = 'localhost'
    query2 = """
            SELECT ?i WHERE {
                ?s <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> food:FoodProduct .
                ?s food:name ?i .
                FILTER(str(?i) != "")
            } LIMIT 10
             """

    @classmethod
    def generate(cls, number):
        parameters = {'offset': randint(0, 10000), 'number': number}
        raw_result = list(Endpoints.query(cls.endpoint2, cls.query2))

        return [Ingredient(label=r[0] or "bonjour",
                           origin=cls.origin.format(word=r[0]),
                           quantity=randint(1, 200),
                           unit=UnitGenerator.generate())
                for r in raw_result]


class UnitGenerator(object):
    # TODO : extraire les unités d'une autre source, voir http://purl.obolibrary.org/obo/uo.owl
    units = (u'mg', u'kg', u'poignées', u'pincées', u'litres', u'hectolitres', u'mm', u'bonnes doses', u'paquets',
             u'cuillerées', u'pelletées', u'centimètres', u'morceaux')

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
                map(rdfSubject.db.add, graph.triples((action.resUri, None, None)))


class TransformedIngredientGenerator(object):
    """
    Génère une liste de transformations avec les ustensiles et ingrédients fournis.
    """

    @classmethod
    def generate(cls, utensils, ingredients):
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
        t = TransformedIngredientGenerator.generate(u, i) if u else []

        return Recipe(person_nb=n, ingredients=i, utensils=u, transformations=t)
