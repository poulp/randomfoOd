from django import template

register = template.Library()

@register.filter
def random_title(recipe):
    return recipe.get_title() 
