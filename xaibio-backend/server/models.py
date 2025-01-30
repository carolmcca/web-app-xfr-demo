from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.contrib.auth.models import User

class Image(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  path = models.TextField()
  hash = models.CharField(max_length=256)
  embedding = ArrayField(models.FloatField())

  def __str__(self):
    return str(self.id)
