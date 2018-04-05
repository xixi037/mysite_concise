from django.db import models

# Create your models here.
class Status(models.Model):
    mode = models.IntegerField()
    date = models.DateField(blank=True, null=True)
    apply_year = models.CharField(max_length=255, blank=True, null=True, default='')