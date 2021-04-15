from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db import models
from .s import *
from .user import *
from django.core.files import File
from django.http import HttpResponse
import numpy as np
from .user_endpoints import photos_path

import base64
import os
import json


@api_view(['POST'])
def searchCategory(request):
    type = json.loads(request.body.decode("utf_8"))
    print(type)
    categories = Workout.objects.filter(category=type)

    listOfDictionaries = []
    for workout in categories:
        listOfDictionaries.append({"id": workout.id, "creatorID": workout.creator_id_id,
                                   "title": workout.title, "caption": workout.caption,
                                   "createdDate": workout.created_date, "category": workout.category
                                   })

    print(listOfDictionaries)
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
        text_file = open(photos_path + user.id, "r")
        pic = text_file.read()
        text_file.close()

        sessionIDs = list(WorkoutSession.objects.filter(user_id__id=user.id).values_list('id', flat=True))
        publishedWorkoutIDs = list(Workout.objects.filter(creator_id__id=user.id).values_list('id', flat=True))

        # liked == [String] where each string is an id of a workout the user liked
        likedWorkouts = list(LikedWorkout.objects.filter(liker_id__id=user.id).values_list('workout_id__id', flat=True))

        listOfDictionaries.append({"id": user.id,
                                   "username": user.username,
                                   "shortBiography": user.bio,
                                   "profilePicture": pic,
                                   "sessionIDs": sessionIDs,
                                   "publishedWorkoutIDs": publishedWorkoutIDs,
                                   "likedWorkoutIDs": likedWorkouts
                                   })
    # print(listOfDictionaries)
    json_string = json.dumps(listOfDictionaries)
    return HttpResponse(json_string)


@api_view(['POST'])
def searchWorkouts(request):
    title_ = json.loads(request.body.decode("utf_8"))

    workouts = Workout.objects.filter(title__startswith=title_)

    listOfDictionaries = []
    for workout in workouts:
        listOfDictionaries.append({"id": workout.id, "creatorID": workout.creator_id_id,
                                   "title": workout.title, "caption": workout.caption,
                                   "createdDate": workout.created_date, "category": workout.category
                                   })

    print(listOfDictionaries)
    json_string = json.dumps(listOfDictionaries)

    return HttpResponse(json_string)

@api_view(['POST'])
def storeSearch(request):
    searchData = json.loads(request.body)
    id = searchData["id"]
    user_iD = searchData["userID"]
    search_item = searchData["keyword"]
    date_item = float(searchData["date"])
    newSearch = SearchHistory.objects.create(id = id, user_id_id = user_iD,searchItem = search_item, date = date_item )
    newSearch.save()
    return HttpResponse("Success")

@api_view(['POST'])
def getSearches(request):
    userId = json.loads(request.body)
    user = userId["userID"]
    results = list(SearchHistory.Objects.filter(user_id = user).values_list('searchItem', flat = True))
    ten = results[-10:]
    json_string = json.dumps(ten)
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
