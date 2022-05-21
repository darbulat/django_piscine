from django.db import models


class Planets(models.Model):
    name = models.CharField(unique=True, max_length=64, null=False)
    climate = models.TextField(null=True)
    diameter = models.IntegerField(null=True)
    population = models.BigIntegerField(null=True)
    orbital_period = models.IntegerField(null=True)
    rotation_period = models.IntegerField(null=True)
    surface_water = models.FloatField(null=True)
    terrain = models.TextField(null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.name
