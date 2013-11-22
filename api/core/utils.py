#!/usr/bin/env python
# -*- coding: utf-8 -*-

from functools import wraps

from rdfalchemy.rdfSubject import rdfSubject
from rdflib import ConjunctiveGraph
from unidecode import unidecode

from constants import RDF_XML


def use_graph(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        rdfSubject.db = ConjunctiveGraph()
        return fn(*args, **kwargs)

    return wrapper


@use_graph
def load_rdf_file(file_name):
    from xml.sax._exceptions import SAXParseException

    try:
        # On charge le fichier
        rdfSubject.db.load(file_name, format=RDF_XML)
    except SAXParseException:
        # Si le fichier est vide on y sauve un graphe vide.
        rdfSubject.db.serialize(destination=file_name, format=RDF_XML)


def get_rdf_graph():
    return rdfSubject.db.serialize(format=RDF_XML)


def save_rdf_file(file_name):
    rdfSubject.db.serialize(file_name, format=RDF_XML)


def sanitize(sentence):
    """
    Permet d'enlever les caractères spéciaux d'une expression pour les URIs.
    """
    return unidecode(unicode(sentence)).replace(' ', '_').replace("'", '').lower()