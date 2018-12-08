from django.db import models

# Create your models here.
from django.db import models


class Room(models.Model):
    name = models.CharField(max_length=100, blank=True, default='')
    count = models.IntegerField(default=0)
