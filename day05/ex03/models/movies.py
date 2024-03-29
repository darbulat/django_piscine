from django.db import models


class Movies(models.Model):
    title = models.CharField(unique=True, max_length=64, null=False)
    episode_nb = models.IntegerField(primary_key=True)
    opening_crawl = models.TextField(null=True)
    director = models.CharField(null=False, max_length=32)
    producer = models.CharField(null=False, max_length=128)
    release_date = models.DateField(null=False)

    def __str__(self) -> str:
        return str(self.title)

