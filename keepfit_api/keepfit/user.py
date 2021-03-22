
from django.db import models

# Create your models here.

class User(models.Model):

    id = models.CharField(max_length=9999,primary_key=True)
    # profile_picture_url = models.CharField(max_length=9999)
    # profile_picture = models.ImageField(upload_to="profile_pictures/")

    weight = models.FloatField()
    height_in_inches = models.IntegerField()

    sex = models.CharField(max_length=80)

    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)

    #birth_date = models.DateField()
    bio = models.CharField(max_length=255)

    #following = models.ManyToManyField(User, symmetrical=False)
    #savedWorkouts = models.ManyToManyField(Workout, symmetrical=False)
    #completedWorkouts = models.ManyToManyField('WorkoutSession', symmetrical=False)

    class Meta:
        db_table = 'user'


class WorkoutSession(models.Model):
    id = models.CharField(max_length=9999,primary_key=True)
    workout_id = models.ForeignKey('Workout', on_delete=models.CASCADE)
    calories = models.FloatField()
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'workout_session'

class Workout(models.Model):
    id = models.CharField(max_length=9999,primary_key=True)
    creator_id = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.IntegerField()
    title = models.CharField(max_length=255)
    caption = models.CharField(max_length=255)

    #def __init__():
    class Meta:
        db_table = 'workout'

