from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db import models
from .s import *
from .models import User
from .models import Workout
from .models import WorkoutSession
from django.core.files import File
from django.http import HttpResponse

import base64
import os
import json

# + func getWorkoutCategories(w http.ResponseWriter, r *http.Request)
# + func getSavedWorkouts(w http.ResponseWriter, r *http.Request)
# + func getCompletedWorkouts(w http.ResponseWriter, r *http.Request)
# + func saveWorkout(w http.ResponseWriter, r *http.Request)
# + func publishWorkout(w http.ResponseWriter, r *http.Request)
# + func downloadWorkoutVideos(w http.ResponseWriter, r *http.Request)
# + func completedWorkout(w http.ResponseWriter, r *http.Request)

# @api_view(['POST'])
# def get_workout_categories(request):
#     json_workouts = json.loads(request.body.decode("utf_8"))
#
#     workout = Workout.objects.filter(id = None)
#
#     if len(workout) < 1:
#         return Response("No Workouts")
#     else:
#         return Response(workout)


@api_view(['POST'])
def getSavedWorkouts(request):
    # not sure if userId will be passed in as well
    json_userId = json.loads(request.body.decode("utf_8"))
    userId = json_userId["userID"]
    user = User.objects.filter(id = userId)
    savedWorkouts = list(user.savedWorkouts.all())
    
    listOfDictionaries = [ob.__dict__ for ob in savedWorkouts]
    json_string = json.dumps(listOfDictionaries)
    return Response(json_string)

@api_view(['POST'])
def getCompletedWorkouts(request):
    json_userId = json.loads(request.body.decode("utf_8"))
    userId = json_userId["userID"]
    user = User.objects.filter(id=userId)
    completedWorkouts = user.completedWorkouts.all()
    if len(completedWorkouts) > 0:
        listOfDictionaries = [ob.__dict__ for ob in completedWorkouts]
        json_string = json.dumps(listOfDictionaries)
        return Response(json_string)
    else:
        return Response("Saved some workouts")


@api_view(['POST'])
def saveWorkout(request):
    json_Workout = json.loads(request.body.decode("utf_8"))
    userId = json_Workout["userID"]
    workoutID = json_Workout["workoutID"]

    user = User.objects.filter(id=userId)
    workout = Workout.objects.filter(id = workoutID)
    if(len(user) == 1):
        user.savedWorkouts.add(workout)
        user.savedWorkouts.save()
        return Response("Success")


@api_view(['POST'])
def publishWorkout(request):
    json_workout = json.loads(request.body.decode("utf_8"))

    video_file = new_user_json["video_file"]
    # save video file to file system for later use

    new_workout = Workout.create (
        id = json_workout["id"],
        title=new_user_json["profile_picture_url"],
        description=new_user_json["weight"],
        category=new_user_json["height_in_inches"],
    )

    new_workout.save()


@api_view(['POST'])
def getWorkout(request):
    json_workoutID = json.loads(request.body.decode("utf_8"))
    wId = json_workoutID[0]
    workout = Workout.objects.filter(id = wId)
    listOfDictionaries = [ob.__dict__ for ob in workout]
    json_string = json.dumps(listOfDictionaries)
    return Response(json_string)

@api_view(['POST'])
def completedWorkout(request):
    js_workout_sess = json.loads(request.body.decode("utf_8"))

    pass




