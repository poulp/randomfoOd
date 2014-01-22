from django.db import models
from django.db.models import Avg
from django.contrib.auth.models import User

class Recipe(models.Model):
    title = models.CharField(max_length=200)
    nb_person = models.IntegerField(default=0)
    ingredients = models.CharField(max_length=2000, default="")
    utensils = models.CharField(max_length=2000, default="")
    transformations = models.CharField(max_length=2000, default="")
    image = models.CharField(max_length=2000, default="")
    user = models.ForeignKey(User)

    def get_rate(self):
        total = Rate.objects.filter(recipe=self).aggregate(Avg('value'))
        if not total["value__avg"]:
            return 0
        else:
            return total["value__avg"]


class Rate(models.Model):
    value = models.IntegerField(default=0)
    user = models.ForeignKey(User)
    recipe = models.ForeignKey(Recipe)

def get_total_rate(recipe):
    
    total = Rate.objects.filter(recipe=recipe).aggregate(Avg('value'))
    if not total["value__avg"]:
        return 0
    else:
        return total["value__avg"]

def get_top_recipe():
    top = Recipe.objects.annotate(top=Avg('rate__value')).order_by('-top')
    return top
    
