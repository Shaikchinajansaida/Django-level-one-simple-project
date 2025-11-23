from django.db import models

# Create your models here.
class Movie_details(models.Model):
    movie_name=models.CharField(max_length=100,unique=True)
    relese_date=models.CharField(max_length=100)
    budget=models.CharField(max_length=100)
    rating=models.FloatField()