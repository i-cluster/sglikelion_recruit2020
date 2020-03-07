from  __future__ import unicode_literals
from django.db import models
from django.utils import timezone

# Create your models here.

class Application(models.Model):
    objects = models.Manager()
    q1 = models.TextField(default="")
    q2 = models.TextField(default="")
    q3 = models.TextField(default="")
    q4 = models.TextField(default="")
    date = models.DateTimeField(default=timezone.now)
    final = models.BooleanField(default=False)
    author = models.CharField(max_length=30)