#!/usr/bin/env python
# -*- coding: utf-8 -*-

from rdfalchemy.rdfSubject import rdfSubject

import constants

from unidecode import unidecode

def load_rdf_file(file_name):
    from xml.sax._exceptions import SAXParseException

    try:
        # On charge le fichier
        rdfSubject.db.load(file_name, format=constants.RDF_XML)
    except SAXParseException:
        # Si le fichier est vide on y sauve un graphe vide.
        rdfSubject.db.serialize(file_name, format=constants.RDF_XML)


def sanitize(sentence):
    """
    Permet d'enlever les caractères spéciaux d'une expression pour les URIs.
    """
    return unidecode(unicode(sentence)).replace(' ', '_').replace("'", '').lower()