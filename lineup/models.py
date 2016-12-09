from __future__ import unicode_literals
from django.db import models


class Key(models.Model):
    mac = models.CharField(max_length=20)
    description = models.CharField(max_length=20, null=True, blank=True)


class Lineup(models.Model):
    zipcode = models.IntegerField()
    provider = models.CharField(max_length=20)

    class Meta:
        unique_together = ('zipcode', 'provider',)


class Channel(models.Model):
    number = models.CharField(max_length=10)
    name = models.CharField(max_length=20)
    icon = models.CharField(max_length=20)
    lineup = models.ForeignKey(Lineup)
