from django.db import models
from django.contrib.auth.models import User

class Recipe(models.Model):
    title = models.CharField(max_length=200)
    nb_person = models.IntegerField(default=0)
    ingredients = models.CharField(max_length=2000, default="")
    utensils = models.CharField(max_length=2000, default="")
    transformations = models.CharField(max_length=2000, default="")
    image = models.CharField(max_length=2000, default="")
    user = models.ForeignKey(User)
