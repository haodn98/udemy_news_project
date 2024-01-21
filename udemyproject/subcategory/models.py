from __future__ import unicode_literals
from django.db import models

# Create your models here.

class SubCategory(models.Model):

    name = models.CharField(max_length=100)
    catname = models.CharField(max_length=100)
    catid = models.IntegerField()

    def __str__(self):
        return f'{self.name}'
