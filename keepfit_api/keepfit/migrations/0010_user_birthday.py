# Generated by Django 3.1.7 on 2021-03-27 23:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('keepfit', '0009_remove_user_birthday'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='birthday',
            field=models.FloatField(default=0.0),
            preserve_default=False,
        ),
    ]
