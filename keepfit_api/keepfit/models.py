from django.db import models

# Create your models here.
class User(models.Model):
    # id = models.IntegerField(primary_key=True)
    # profile_picture_url = models.CharField(max_length=9999)
    # profile_picture = models.ImageField(upload_to="profile_pictures/")

    weight = models.FloatField()
    height_in_inches = models.IntegerField()

    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    
    birth_date = models.DateField()

    class Meta:
        db_table = 'user'

    # def save(self):
    #     models.Model.save(self)
    #     return self.pk
    #
    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)  # Call the "real" save() method.
    #
