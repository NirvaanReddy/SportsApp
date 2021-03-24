# Generated by Django 3.1.7 on 2021-03-22 21:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('keepfit', '0003_auto_20210322_0624'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='birth_date',
        ),
        migrations.RemoveField(
            model_name='user',
            name='completedWorkouts',
        ),
        migrations.AddField(
            model_name='user',
            name='bio',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='sex',
            field=models.CharField(default='Male', max_length=80),
            preserve_default=False,
        ),
    ]