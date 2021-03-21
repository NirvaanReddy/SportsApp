from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db import models
from .s import *
from .models import *
from django.core.files import File

import base64
import os
import json
#
def searchCategory(request):
    name_json = json.loads(request.body.decode("utf_8"))
    type = name_json["category"]
    categories = Workout.objects.filter(category = type)
    if len(categories != 1):
        return categories
    else:
        return ("notfound")


def searchUsers(request):
    name_json = json.loads(request.body.decode("utf_8"))
    name = name_json["username"] #name is now a string of the sent username
    users = User.objects.filter(username=name)
    # If the username exists
    if len(users) !=0:
        return users
    else:
        return Response("notfound")

def searchWorkouts(request):
    name_json = json.loads(request.body.decode("utf_8"))
    caption_ = name_json["workout"]
    workout = Workout.objects.filter(caption=caption_)
    if len(workout) != 0:
        return workout
    else:
        return Response("notfound")
