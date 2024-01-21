from __future__ import unicode_literals
from django.db import models
import datetime


class News(models.Model):
    name = models.CharField(max_length=200)
    short_txt = models.TextField()
    body_txt = models.TextField()
    date = models.CharField(max_length=30)
    picname = models.TextField()
    picurl = models.TextField(default='-')
    writer = models.CharField(max_length=50)
    catname = models.CharField(max_length=100, default='-')
    catid = models.IntegerField(default=0)
    ocatid = models.IntegerField(default=0)
    show = models.IntegerField(default=0)
    act = models.IntegerField(default=0)
    tag = models.TextField(default='')
    rand = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.name}"
