from django.db import models
from django import utils


# Create your models here.
class Job(models.Model):
    # need to add user search
    search = models.CharField(max_length=200)
    link = models.CharField(max_length=2083)
    title = models.CharField(max_length=200)
    pay = models.CharField(max_length=200)
    type = models.CharField(max_length=200)
    board = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    difficulty = models.CharField(max_length=200)
    date = models.DateTimeField(default=utils.timezone.now)
    radius = models.CharField(max_length=3)

    def __str__(self):
        return self.title
