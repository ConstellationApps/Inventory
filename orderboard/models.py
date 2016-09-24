from django.db import models

# Create your models here.

class item(models.Model):
    name = models.CharField(max_length=128)
    quantity = models.IntegerField()
    notes = models.TextField()
