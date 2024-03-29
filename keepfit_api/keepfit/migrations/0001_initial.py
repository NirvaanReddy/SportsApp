# Generated by Django 3.1.7 on 2021-03-19 00:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weight', models.FloatField()),
                ('heightInInches', models.IntegerField()),
                ('username', models.CharField(max_length=255)),
                ('password', models.CharField(max_length=255)),
                ('birth_date', models.DateField()),
            ],
            options={
                'db_table': 'user',
            },
        ),
    ]
