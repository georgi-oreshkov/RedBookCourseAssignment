# models.py
from django.db import models
from django.contrib.auth.models import User


class Species(models.Model):
    name = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='species_images')
    sp_type = models.CharField(max_length=25)

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    species = models.ForeignKey(Species, on_delete=models.CASCADE)


