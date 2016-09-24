from django.db import models

# Create your models here.

class Item(models.Model):
    name = models.CharField(max_length=128)
    quantity = models.IntegerField()
    notes = models.TextField()
