from django.db import models

from . import People


class Movies(models.Model):

    title = models.CharField(unique=True, max_length=64, null=False)
    episode_nb = models.IntegerField(primary_key=True)
    opening_crawl = models.TextField(null=True)
    director = models.CharField(null=False, max_length=32)
    producer = models.CharField(null=False, max_length=128)
    release_date = models.DateField(null=False)
    characters = models.ManyToManyField(to=People)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        default_related_name = 'movies'

    def __str__(self) -> str:
        return str(self.title)
