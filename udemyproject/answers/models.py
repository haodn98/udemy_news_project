from django.db import models


# Create your models here.

class Answer(models.Model):
    to_email = models.CharField(max_length=50, default="")
    answer_txt = models.TextField(default="")
    date = models.CharField(max_length=50, default="")
