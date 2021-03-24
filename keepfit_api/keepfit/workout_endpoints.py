from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db import models
from .s import *
from .user import User
from .user import Workout
from .user import WorkoutSession
from .user import savedWorkout
from .user import likedWorkout
from .user import completedWorkout
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
    # assuming workou
    json_userId = json.loads(request.body.decode("utf_8"))
    userId = json_userId["userID"]
    savedWorkouts = Workout.objects.filter(saved_workouts__saver_id = userId)
    listOfDictionaries = [ob.__dict__ for ob in savedWorkouts]
    json_string = json.dumps(listOfDictionaries)
    return Response(json_string)

@api_view(['POST'])
def getCompletedWorkouts(request):
    json_userId = json.loads(request.body.decode("utf_8"))
    userId = json_userId["userID"]
    completedWorkouts = WorkoutSession.objects.filter(user_id=userId)
    listOfDictionaries = [ob.__dict__ for ob in completedWorkouts]
    json_string = json.dumps(listOfDictionaries)
    return Response(json_string)

def getLikedWorkouts(request):
    json_userId = json.loads(request.body.decode("utf_8"))
    userId = json_userId["userID"]
    liked = Workout.objects.filter(liked_workouts__liker_id=userId)
    listOfDictionaries = [ob.__dict__ for ob in liked]
    json_string = json.dumps(listOfDictionaries)
    return Response(json_string)

@api_view(['POST'])
def saveWorkout(request):
    # assume workout Id and User ID passed in
    json_Workout = json.loads(request.body.decode("utf_8"))
    userId = json_Workout["userID"]
    wID = json_Workout["workoutID"]
    newWorkout = savedWorkout.create(saver_id = userId, workout_id = wID)
    newWorkout.save()
    return Response("Success")


@api_view(['POST'])
def likeWorkout(request):
    # assume workout Id and User ID passed in
    json_Workout = json.loads(request.body.decode("utf_8"))
    userId = json_Workout["userID"]
    wID = json_Workout["workoutID"]
    newWorkout = likedWorkout.create(liker_id=userId, workout_id=wID)
    newWorkout.save()
    return Response("Success")

@api_view(['POST'])
def completeWorkout(request):
    # assume workout Id and User ID passed in
    json_Workout = json.loads(request.body.decode("utf_8"))
    userId = json_Workout["userID"]
    wID = json_Workout["workoutID"]
    calories = int(json_Workout["calories"])
    newWorkout = WorkoutSession.create(id = json_Workout["workoutSessionID"],workout_id= wID,
                                       user_id=userId,
                                       category= int(json_Workout["category"]),
                                       title = json_Workout["title"],
                                       caption = json_Workout["caption"]
                                       )
    newWorkout.save()
    return Response("Success")


@api_view(['POST'])
def publishWorkout(request):
    workout_json = json.loads(request.body.decode("utf_8"))

    video_file = workout_json["video_file"]
    # save video file to file system for later use

    new_workout = Workout.create (
        id = workout_json["workout_id"],
        title=workout_json["profile_picture_url"],
        creater_id = workout_json["user_id"],
        caption=workout_json["caption"],
        category=workout_json["category"],
    )

    new_workout.save()
    return Response("Success")


@api_view(['POST'])
def getWorkout(request):
    json_workoutID = json.loads(request.body.decode("utf_8"))
    wId = json_workoutID["workoutID"]
    workout = Workout.objects.filter(id = wId)
    listOfDictionaries = [ob.__dict__ for ob in workout]
    json_string = json.dumps(listOfDictionaries)
    return Response(json_string)


def postVideo(request):
    js_workout_vid = json.loads(request.body)
    filename = js_workout_vid[0]
    binary_data = js_workout_vid[1]
    path_name = 'path/videos/'
    new_file = open(path_name + filename,'x')
    new_file.write(binary_data)
    new_file.close()
    worked = True
    try:
        r = open(path_name + filename, 'r')
    except IOError:
        worked = False

    if worked:
        return Response(True)
    else:
        return Response(False)

    # json object w/2 things
    # 1st thing unique file name
    # 2nd thing is gonna be binary data




def downloadVideo(request):
    js_workout = json.loads(request.body)
    filename =
    pathname = 'path/videos/'






