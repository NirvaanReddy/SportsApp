from django.db import models

# Create your models here.
from models.py import Workout
from models.py import WorkoutSession
from models.py import User


class User(models.Model):
    id = models.CharField(primary_key=True)
    # profile_picture_url = models.CharField(max_length=9999)
    # profile_picture = models.ImageField(upload_to="profile_pictures/")

    weight = models.FloatField()
    height_in_inches = models.IntegerField()

    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)

    birth_date = models.DateField()

    following = models.ManyToManyField(__self__, symmetrical=False)
    savedWorkouts = models.ManyToManyField(Workout, symmetrical=False)
    completedWorkouts = models.ManyToManyField(WorkoutSession, symmetrical=False)

    class Meta:
        db_table = 'user'


class Workout(models.Model):
    id = models.CharField(primary_key=True)
    creator_id = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.IntegerField()
    title = models.CharField(max_length=255)
    caption = models.CharField(max_length=255)

    #def __init__():
    class Meta:
        db_table = 'Workout'

class WorkoutSession(models.Model):
    id = models.CharField(primary_key=True)
    workout_id = models.ForeignKey(Workout, on_delete=models.CASCADE)
    calories = models.FloatField()
    exerciser_id = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'WorkoutSession'




    # def save(self):
    #     models.Model.save(self)
    #     return self.pk
    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)  # Call the "real" save() method.

#x = Workout.objects.filter(category=2).sortByDate().filter(top10)
#for workout in x:
#    jsonData = jsonify(workout)
#    put in lost(jsonData)
#send back listofjsondata


