from django.db import models

# Create your models here.

class Item(models.Model):
    LIFECYCLE_STAGES=[('W', "Wanted"),
                      ('O', "Ordered"),
                      ('R', "Recieved")]

    name = models.CharField(max_length=128)
    quantity = models.IntegerField()
    notes = models.TextField()
    stage = models.CharField(max_length=1, choices=LIFECYCLE_STAGES, default='W')
