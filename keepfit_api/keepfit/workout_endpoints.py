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

@api_view(['POST'])
def get_workout_categories(request):
    json_workouts = json.loads(request.body.decode("utf_8"))

    workout = Workout.objects.filter(id = None)

    if len(workout) < 1:
        return Response("No Workouts")
    else:
        return Response(workout)


@api_view(['POST'])
def getSavedWorkouts(request):
    # not sure if userId will be passed in as well
    json_userId = json.loads(request.body.decode("utf_8"))
    userId = json_userId[0]
    user = User.objects.filter(id = userId)
    savedWorkouts =  user.savedWorkouts.all()
    if len(savedWorkouts) > 0:
        return Response(savedWorkouts)
    else:
        return Response("Saved some workouts")

@api_view(['POST'])
def getCompletedWorkouts( request):
    json_userId = json.loads(request.body.decode("utf_8"))
    userId = json_userId[0]
    user = User.objects.filter(id=userId)
    completedWorkouts = user.completedWorkouts.all()
    if len(completedWorkouts) > 0:
        return Response(completedWorkouts)
    else:
        return Response("Saved some workouts")


@api_view(['POST'])
def saveWorkout(request):
    json_Workout = json.loads(request.body.decode("utf_8"))
    userId = json_Workout[0]
    workout_id = json_Workout[1]
    user = User.objects.filter(id=userId)

    user.savedWorkouts.add

@api_view(['POST'])
def publishWorkout( rWriter, hRequest):
    pass

@api_view(['POST'])
def downloadWorkoutVideos( rWriter, hRequest):
    pass

@api_view(['POST'])
def completedWorkout( rWriter, hRequest):
    pass







