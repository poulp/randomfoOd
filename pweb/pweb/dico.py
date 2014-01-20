#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'cyril'

import urllib2
import xml.etree.ElementTree as ET

def init(keyword):
    queryHTML = 'http://fr.wiktionary.org/wiki/'+keyword
    HTMLresponse = urllib2.urlopen(queryHTML)
    return ET.fromstring(HTMLresponse.read())


def findPlurial(root):
    """
    Retourne le pluriel d'un mot singulier, ou le singulier d'un mot au pluriel.
    """
    for table in root.iter('table'):
        if table.get('class') == "flextable flextable-fr-mfsp":
            for td in table.iter('a'):
                return td.get('title')

def findKind(root):
    """
    Retourn m : masculin ou f : pour féminin.
    """
    for i in root.iter('i'):
        if i.text == "masculin" or i.text == "féminin":
            return i.text[0]


## Exemple d'utilisation ##
keyword = "porte"
root = init(keyword)
print findPlurial(root)
print findKind(root)

keyword = "sucre"
root = init(keyword)
print findPlurial(root)
print findKind(root)

keyword = "tableau"
root = init(keyword)
print findPlurial(root)
print findKind(root)