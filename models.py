from django.db import models

class Card(models.Model):
    name = models.CharField(max_length=128)
    quantity = models.IntegerField(default=1)
    notes = models.TextField()
    stage = models.ForeignKey('Stage', blank=True, null=True)
    board = models.ForeignKey('Board', blank=True, null=True)
    archived = models.BooleanField(default=False)
    
class Board(models.Model):
    name = models.CharField(max_length=128)
    desc = models.TextField()
    active = models.BooleanField(default=True)
    
class Stage(models.Model):
    name = models.CharField(max_length=128)
    index = models.IntegerField()
    archived = models.BooleanField(default=False)
