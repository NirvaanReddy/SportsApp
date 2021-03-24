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


# @api_view(['POST'])
# def getSavedWorkouts(request):
#     # not sure if userId will be passed in as well
#     # assuming workou
#     json_userId = json.loads(request.body.decode("utf_8"))
#     userId = json_userId["userID"]
#     savedWorkouts = Workout.objects.filter(saved_workouts__saver_id = userId)
#     listOfDictionaries = [ob.__dict__ for ob in savedWorkouts]
#     json_string = json.dumps(listOfDictionaries)
#     return HttpResponse(json_string)
#
# @api_view(['POST'])
# def getCompletedWorkouts(request):
#     json_userId = json.loads(request.body.decode("utf_8"))
#     userId = json_userId["userID"]
#     completedWorkouts = WorkoutSession.objects.filter(user_id=userId)
#     listOfDictionaries = [ob.__dict__ for ob in completedWorkouts]
#     json_string = json.dumps(listOfDictionaries)
#     return HttpResponse(json_string)
#
# def getLikedWorkouts(request):
#     json_userId = json.loads(request.body.decode("utf_8"))
#     userId = json_userId["userID"]
#     liked = Workout.objects.filter(liked_workouts__liker_id=userId)
#     listOfDictionaries = [ob.__dict__ for ob in liked]
#     json_string = json.dumps(listOfDictionaries)
#     return HttpResponse(json_string)

@api_view(['POST'])
def saveWorkout(request):
    # assume workout Id and User ID passed in
    json_Workout = json.loads(request.body.decode("utf_8"))
    userId = json_Workout["userID"]
    wID = json_Workout["workoutID"]
    newWorkout = savedWorkout.create(saver_id = userId, workout_id = wID)
    newWorkout.save()
    return HttpResponse("Success")


@api_view(['POST'])
def likeWorkout(request):
    # assume workout Id and User ID passed in
    json_Workout = json.loads(request.body.decode("utf_8"))
    userId = json_Workout["userID"]
    wID = json_Workout["workoutID"]
    newWorkout = likedWorkout.create(liker_id=userId, workout_id=wID)
    newWorkout.save()
    return HttpResponse("Success")

@api_view(['POST'])
def completeWorkout(request):
    # assume workout Id and User ID passed in
    json_Workout = json.loads(request.body.decode("utf_8"))
    userId = json_Workout["userID"]
    wID = json_Workout["workoutID"]
    calories = json_Workout["calories"]
    newWorkout = WorkoutSession.create(id = json_Workout["workoutSessionID"],workout_id= wID,
                                       user_id=userId,
                                       category= json_Workout["category"],
                                       title = json_Workout["title"],
                                       caption = json_Workout["caption"],

                                       )
    newWorkout.save()
    return HttpResponse("Success")


@api_view(['POST'])
def publishWorkout(request):
    workout_json = json.loads(request.body.decode("utf_8"))

    new_workout = Workout.create (
        id = workout_json["id"],
        title=workout_json["title"],
        creator_id = workout_json["creatorID"],
        caption=workout_json["caption"],
        category=workout_json["category"],
        start_time=workout_json["createdDate"]
    )

    new_workout.save()
    return HttpResponse("Success")

@api_view(['POST'])
def getWorkoutSession(request):
    wsID = json.loads(request.body.decode("utf_8"))

    # WorkoutSession
    # {
    #     id: String
    #     workoutID: String
    #     userID: String
    #     startTime: Double
    #     endTime: Double
    #     caloriesBurned: Integer
    # }

    workout_session = WorkoutSession.objects.filter(id=wsID)
    ws_dict = {"id": workout_session.id, "workoutID": workout_session.workout_id,
               "userID": workout_session.userID, "startTime": workout_session.start_time,
               "endTime": workout_session.end_time }
    json_string = json.dumps(ws_dict)
    return HttpResponse(json_string)


@api_view(['POST'])
def getWorkout(request):
    wID = json.loads(request.body.decode("utf_8"))

    # Workout
    # {
    #     id: String
    #     creatorID: String
    #
    #     createdDate: Double // dates are stored as doubles
    # title: String
    # caption: String
    # category: String
    # }

    workout = Workout.objects.filter(id = wID)
    workout_dict = { "id" : workout.id, "creatorID": workout.creater_id,
                            "title": workout.title, "caption": workout.caption,
                            "createdDate": workout.createdDate, "category": workout.category
                        }

    json_string = json.dumps(workout_dict)
    return HttpResponse(json_string)


def postVideo(request):
    js_workout_vid = json.loads(request.body)
    filename = js_workout_vid["workoutID"]
    binary_data = js_workout_vid["videoData"]
    path_name = '/home/ec2-user/videos/'
    new_file = open(path_name + filename,'w')
    new_file.write(binary_data)
    new_file.close()
    worked = True
    try:
        r = open(path_name + filename, 'r')
    except IOError:
        worked = False

    if worked:
        return HttpResponse("True")
    else:
        return HttpResponse("False")

    # json object w/2 things
    # 1st thing unique file name
    # 2nd thing is gonna be binary data




def downloadVideo(request):
    file_name = json.loads(request.body)
    path_name = '/home/ec2-user/videos/'
    new_file = open(path_name + file_name,'r')
    binary_data = new_file.read()
    new_file.close()

    return HttpResponse(binary_data)






