#!/usr/bin/env python
# -*- coding: utf-8 -*-

from xml.sax._exceptions import SAXParseException
from functools import wraps

from rdfalchemy.rdfSubject import rdfSubject
from rdflib import ConjunctiveGraph, URIRef
from unidecode import unidecode
from flask import request
from werkzeug.exceptions import UnsupportedMediaType, NotAcceptable
from constants import RDF_XML


##### DÉCORATEURS
def consumes(*content_types):
    """
    Ajoute une vérification des headers Content-Type de la requête.
    """

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
    """
    Ajoute une vérification des headers Accept de la requête.
    """

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
    """
    Réinitialise le graphe global de rdfalchemy.
    """

    @wraps(fn)
    def wrapper(*args, **kwargs):
        rdfSubject.db = ConjunctiveGraph()
        return fn(*args, **kwargs)

    wrapper.truc = 67
    return wrapper


##### AUTRE
def load_rdf_file(filename, graph=None):
    """
    Charge le fichier dans le graphe donné.
    Si aucun graphe n'est donné, charge dans le graphe global.
    """
    if graph is None:
        graph = rdfSubject.db

    try:
        # On charge le fichier
        graph.load(filename, format=RDF_XML)
    except SAXParseException:
        # Si le fichier est vide on y sauve un graphe vide.
        graph.db = ConjunctiveGraph()
        graph.db.serialize(destination=filename, format=RDF_XML)


def get_rdf_graph(graph=None):
    """
    Renvoie le graphe donné sérializé au format RDF.
    Si aucun graphe n'est donné, sérialize le graphe global.
    """
    if graph is None:
        graph = rdfSubject.db

    return graph.serialize(format=RDF_XML)


def save_rdf_file(filename, graph=None):
    """
    Sauveagrde le graphe dans le fichier donné.
    Si aucun graphe n'est donné, sauvegarde le graphe global.
    """
    if graph is None:
        graph = rdfSubject.db

    graph.serialize(filename, format=RDF_XML)


def sanitize(sentence):
    """
    Permet d'enlever les caractères spéciaux d'une expression pour les URIs.
    """
    return unidecode(unicode(sentence)).replace(' ', '_').replace("'", '').lower()


def create_uri(uri):
    """
    Renvoie un objet URI manipulable par rdflib et rdfalchemy.
    """
    return URIRef(uri)

