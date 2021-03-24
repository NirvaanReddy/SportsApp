from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db import models
from .s import *
from .user import *
from django.core.files import File

import base64
import os
import json


@api_view(['POST'])
def searchCategory(request):
    name_json = json.loads(request.body.decode("utf_8"))
    type = name_json["category"]
    categories = list(Workout.objects.filter(category=type))

    #convert to json
    listOfDictionaries = [ob.__dict__ for ob in categories]
    json_string = json.dumps(listOfDictionaries)

    return Response(json_string)
    #https://pythonexamples.org/python-list-to-json/#3


@api_view(['POST'])
def searchUsers(request):
    name_json = json.loads(request.body.decode("utf_8"))
    name = name_json["username"] #name is now a string of the sent username
    users = list(User.objects.filter(username=name))
    # If the username exists
    listOfDictionaries = [ob.__dict__ for ob in users]
    json_string = json.dumps(listOfDictionaries)
    return Response(json_string)

@api_view(['POST'])
def searchWorkouts(request):
    name_json = json.loads(request.body.decode("utf_8"))
    title_ = name_json["workout"]
    workout = Workout.objects.filter(title=title_)
    dict = [ob.__dict__ for ob in workout]
    json_string = json.dumps(dict)

    return Response(json_string)

#
#
#
#
#
#
#
#
#