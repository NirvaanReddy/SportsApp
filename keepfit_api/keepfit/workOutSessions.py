from django.db import models
from models.py import User
from w.py import Workout

class WorkoutSession(models.Model):
    id = models.CharField(primary_key=True)
    workout_id = models.ForeignKey(Workout, on_delete=models.CASCADE)
    calories = models.FloatField()
    exerciser_id = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'WorkoutSession'

