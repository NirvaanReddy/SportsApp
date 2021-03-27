from django.db import models


# Create your models here.

class User(models.Model):
    id = models.CharField(max_length=9999, primary_key=True)
    # profile_picture_url = models.CharField(max_length=9999)
    # profile_picture = models.ImageField(upload_to="profile_pictures/")
    height_in_inches = models.IntegerField()
    sex = models.CharField(max_length=80)
    weight = models.FloatField()

    # profilePicture removed
    # profilePicture = models.CharField(max_length=255, unique=False)

    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    birthday = models.FloatField()
    bio = models.CharField(max_length=255)

    # following = models.ManyToManyField(User, symmetrical=False)
    # savedWorkouts = models.ManyToManyField(Workout, symmetrical=False)
    # completedWorkouts = models.ManyToManyField('WorkoutSession', symmetrical=False)

    class Meta:
        db_table = 'user'


class WorkoutSession(models.Model):
    id = models.CharField(max_length=9999, primary_key=True)
    workout_id = models.ForeignKey('Workout', on_delete=models.CASCADE)
    calories = models.FloatField()
    user_id = models.ForeignKey('User', on_delete=models.CASCADE)
    # Start and end time added
    start_time = models.FloatField()
    end_time = models.FloatField()

    class Meta:
        db_table = 'workout_session'


class Workout(models.Model):
    id = models.CharField(max_length=9999, primary_key=True)
    creator_id = models.ForeignKey('User', on_delete=models.CASCADE)
    category = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    caption = models.CharField(max_length=255)
    created_date = models.FloatField()

    class Meta:
        db_table = 'workout'


# class SavedWorkout(models.Model):
#     saver_id = models.ForeignKey('User', on_delete=models.CASCADE)
#     workout_id = models.ForeignKey('Workout', on_delete=models.CASCADE)
#
#     class Meta:
#         db_table = 'saved_workouts'


class LikedWorkout(models.Model):
    liker_id = models.ForeignKey('User', on_delete=models.CASCADE)
    workout_id = models.ForeignKey('Workout', on_delete=models.CASCADE)

    class Meta:
        db_table = 'liked_workouts'


# class CompletedWorkout(models.Model):
#     completer_id = models.ForeignKey('User', on_delete=models.CASCADE)
#     workout_id = models.ForeignKey('Workout', on_delete=models.CASCADE)
#
#     class Meta:
#         db_table = 'completed_workouts'


class Following(models.Model):
    follower = models.ForeignKey('User', on_delete=models.CASCADE, related_name='p1')
    following = models.ForeignKey('User', on_delete=models.CASCADE, related_name='p2')

    class Meta:
        db_table = 'followings'
