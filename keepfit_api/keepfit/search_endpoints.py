from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db import models
from .s import *
from .user import *
from django.core.files import File
from .user import completedWorkout
from django.core.files import File
from django.http import HttpResponse

import base64
import os
import json


@api_view(['POST'])
def searchCategory(request):
    name_json = json.loads(request.body.decode("utf_8"))
    type = name_json["category"]
    categories = Workout.objects.filter(category=type)

    listOfDictionaries = []
    for workout in categories:
        listOfDictionaries.append({"id": workout.id, "creatorID": workout.creater_id,
                                   "title": workout.title, "caption": workout.caption,
                                   "createdDate": workout.createdDate, "category": workout.category
                                   })

    json_string = json.dumps(listOfDictionaries)

    return HttpResponse(json_string)
    # https://pythonexamples.org/python-list-to-json/#3


@api_view(['POST'])
def searchUsers(request):
    name = json.loads(request.body.decode("utf_8"))
    # name is now a string of the sent username
    users = User.objects.filter(username__startswith=name)

    # UserPreview
    # {
    #     id: String
    #     username: String
    #
    #     shortBiography: String
    #
    #     profilePicture: String
    #
    #     sessionIDs: [String]
    #     likedWorkoutIDs: [String]
    #     publishedWorkoutIDs: [String]
    # }

    listOfDictionaries = []
    for user in users:
        text_file = open("/home/ec2-user/photos/" + user.id, "r")
        pic = text_file.read()
        text_file.close()

        published_workouts = Workout.objects.filter(user__creater_id=user.id).values("id").values_list('id', flat=True)
        sessionIDs = WorkoutSession.objects.filter(user__user_id=user.id).values("id").values_list('id', flat=True)
        likedWorkouts = Workout.objects.(user__=user.id).values("id").values_list('id', flat = True)
        listOfDictionaries.append({"id": user.id, "username": user.username,
                                   "shortBiography": user.shortBiography, "profilePicture": pic,
                                   "sessionIDs": sessionIDs, "likedWorkoutsIDs": likedWorkouts,
                                    "publishedWorkoutIDs": published_workouts
        })

        json_string = json.dumps(listOfDictionaries)
        return HttpResponse(json_string)

    @api_view(['POST'])
    def searchWorkouts(request):
        title_ = json.loads(request.body.decode("utf_8"))

        workouts = Workout.objects.filter(title__startswith=title_)

        listOfDictionaries = []
        for workout in workouts:
            listOfDictionaries.append({"id": workout.id, "creatorID": workout.creater_id,
                                       "title": workout.title, "caption": workout.caption,
                                       "createdDate": workout.createdDate, "category": workout.category
                                       })

        json_string = json.dumps(dict)

        return HttpResponse(json_string)

    #
    #
    #
    #
    #
    #
    #
    #
    #