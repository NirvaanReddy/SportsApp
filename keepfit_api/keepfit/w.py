from django.db import models
from models.py import User

class Workout(models.Model):
    id = models.CharField(primary_key=True)
    creator_id = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.IntegerField()
    title = models.CharField(max_length=255)
    caption = models.CharField(max_length=255)

    #def __init__():
    class Meta:
        db_table = 'Workout'