from __future__ import unicode_literals
from django.db import models


# Create your models here.

class ContactForm(models.Model):

    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    message = models.TextField(default="-")
    date = models.CharField(max_length=30,default="-")

    def __str__(self):
        return f"{self.pk} {self.name}"