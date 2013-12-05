from django import template
from ..syntax import link_ingredient

register = template.Library()


@register.filter
def random_title(recipe):
    return recipe.get_title()


@register.filter
def display_ingredient(ingredient):
    return link_ingredient(ingredient)
