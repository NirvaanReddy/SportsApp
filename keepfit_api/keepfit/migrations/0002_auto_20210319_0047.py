# Generated by Django 3.1.7 on 2021-03-19 00:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('keepfit', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
