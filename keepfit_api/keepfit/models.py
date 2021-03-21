from django.db import models

# Create your models here.
class User(models.Model):

    id = models.IntegerField(primary_key=True)
    # profile_picture_url = models.CharField(max_length=9999)
    # profile_picture = models.ImageField(upload_to="profile_pictures/")

    weight = models.FloatField()
    height_in_inches = models.IntegerField()

    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    
    birth_date = models.DateField()

    following = models.ManyToManyField(User, symmetrical=False)

    class Meta:
        db_table = 'user'

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

class Workout(models.Model):
    id = models.IntegerField(primary_key=True)
    creator_id = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.IntegerField()
    caption = models.CharField(max_length=True)

    class Meta:
        db_table = 'Workout'

class WorkoutSession(models.Model):
    id = models.IntegerField(primary_key=True)
    calories = models.FloatField()
    exerciser_id = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'WorkoutSession'


