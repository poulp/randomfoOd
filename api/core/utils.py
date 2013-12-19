#!/usr/bin/env python
# -*- coding: utf-8 -*-

from xml.sax._exceptions import SAXParseException
from functools import wraps

from rdfalchemy.rdfSubject import rdfSubject
from rdflib import ConjunctiveGraph
from unidecode import unidecode
from flask import request
from werkzeug.exceptions import UnsupportedMediaType, NotAcceptable

from constants import RDF_XML


##### DÉCORATEURS
def consumes(*content_types):
    def decorated(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            if request.mimetype not in content_types:
                raise UnsupportedMediaType()

            return fn(*args, **kwargs)

        wrapper.consumes = content_types
        return wrapper

    return decorated


def produces(*content_types):
    def decorated(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            requested = set(request.accept_mimetypes.values())
            defined = set(content_types)
            if len(requested & defined) == 0:
                raise NotAcceptable()
            return fn(*args, **kwargs)

        wrapper.produces = content_types
        return wrapper

    return decorated


def reset_graph(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        rdfSubject.db = ConjunctiveGraph()
        return fn(*args, **kwargs)
    wrapper.truc = 67
    return wrapper


##### AUTRE
def load_rdf_file(file_name, graph=None):
    if graph is None:
        graph = rdfSubject.db

    try:
        # On charge le fichier
        graph.load(file_name, format=RDF_XML)
    except SAXParseException:
        # Si le fichier est vide on y sauve un graphe vide.
        graph.db = ConjunctiveGraph()
        graph.db.serialize(destination=file_name, format=RDF_XML)


def get_rdf_graph(graph=None):
    if graph is None:
        graph = rdfSubject.db

    return graph.serialize(format=RDF_XML)


def save_rdf_file(file_name, graph=None):
    if graph is None:
        graph = rdfSubject.db

    graph.serialize(file_name, format=RDF_XML)


def sanitize(sentence):
    """
    Permet d'enlever les caractères spéciaux d'une expression pour les URIs.
    """
    return unidecode(unicode(sentence)).replace(' ', '_').replace("'", '').lower()

