from django.db import models

# Create your models here.

class location(models.Model):
    id = models.AutoField(primary_key=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    name = models.TextField()
    description = models.TextField()
    address = models.TextField()
    category = models.TextField()
    class Meta:
        db_table = 'location'