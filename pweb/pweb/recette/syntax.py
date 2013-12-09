# -*- coding:utf8 -*-

# Fichier contenant des fonctions et constantes
# pour assurer les corréctions de syntaxe française

VOYELLE = ['a', 'e', 'i', 'o', 'u', 'é', 'è']


# construction du titre de la recette
def link_title_recipe(string1, string2):
    if string2[0].lower() in VOYELLE:
        return string1.capitalize() + u" à l'" + string2
    else:
        return string1.capitalize() + u" à la " + string2


def link_ingredient(string):
    if string[0].lower() in VOYELLE:
        return u" d'" + string
    else:
        return u" de " + string
