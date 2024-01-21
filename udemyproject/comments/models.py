from django.db import models

# Create your models here.
class Comment(models.Model):
    cm = models.TextField()
    name = models.CharField(max_length=50)
    news_id = models.IntegerField()
    email = models.CharField(max_length=50,default="")
    date = models.CharField(max_length=50)
    status = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.name} | {str(self.pk)}"
