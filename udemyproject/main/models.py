from __future__ import unicode_literals
from django.db import models


class Main(models.Model):
    name = models.CharField(max_length=30)
    short_about = models.CharField(max_length=100,default="-")
    about = models.TextField(default="-")
    fb = models.CharField(max_length=100, default='-')
    tw = models.CharField(max_length=100, default='-')
    yt = models.CharField(max_length=100, default='-')
    tell = models.CharField(max_length=100, default='-')
    link = models.CharField(max_length=100, default='-')
    set_name = models.CharField(max_length=100, default='-')
    picurl = models.TextField(default="")
    picname = models.TextField(default="")
    picurl2 = models.TextField(default="")
    picname2 = models.TextField(default="")
    seo_txt= models.CharField(default="-",max_length=200)
    seo_key_words = models.TextField(default="-")

    def __str__(self):
        return f"{str(self.pk)}. {self.set_name}"
