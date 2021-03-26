from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db import models
from .s import *
from .user import *
from django.core.files import File
from django.http import HttpResponse

import base64
import os
import json


# videos_path = "~/Desktop/TempVids/"
videos_path = "/home/ec2-user/videos/"

@api_view(['POST'])
def likeWorkout(request):
    # assume workout Id and User ID passed in
    json_Workout = json.loads(request.body.decode("utf_8"))
    userId = json_Workout["userID"]
    wID = json_Workout["workoutID"]
    user = User.objects.get(id=userId)
    workout = Workout.objects.get(id=wID)
    newWorkout = LikedWorkout.objects.create(liker_id=user, workout_id=workout)
    newWorkout.save()
    return HttpResponse("Success")

@api_view(['POST'])
def unlikeWorkout(request):
    # assume workout Id and User ID passed in
    json_Workout = json.loads(request.body.decode("utf_8"))
    userId = json_Workout["userID"]
    wID = json_Workout["workoutID"]

    oldWorkout = LikedWorkout.objects.get(liker_id_id=userId, workout_id_id=wID)
    oldWorkout.delete()
    return HttpResponse("Success")

@api_view(['POST'])
def completeWorkout(request):
    # inputs WorkoutSession JSON

    # WorkoutSession
    # {
    #     id: String
    #     workoutID: String
    #     userID: String
    #     startTime: Double
    #     endTime: Double
    #     caloriesBurned: Integer
    # }

    json_Workout = json.loads(request.body.decode("utf_8"))

    newWorkout = WorkoutSession.objects.create(id=json_Workout["id"],
                                       workout_id_id=json_Workout["workoutID"],
                                       calories=json_Workout["caloriesBurned"],
                                       user_id_id=json_Workout["userID"],
                                       start_time=json_Workout["startTime"],
                                       end_time=json_Workout["endTime"]
                                       )
    newWorkout.save()
    return HttpResponse("Success")


@api_view(['POST'])
def publishWorkout(request):
    workout_json = json.loads(request.body.decode("utf_8"))

    # Workout
    # {
    # id: String
    # creatorID: String
    #
    # createdDate: Double // dates are stored as doubles
    # title: String
    # caption: String
    # category: String
    # }

    # creator = User.objects.get(id=workout_json["creatorID"])
    new_workout = Workout.objects.create(
        id=workout_json["id"],
        title=workout_json["title"],
        creator_id_id=workout_json["creatorID"],
        caption=workout_json["caption"],
        category=workout_json["category"],
        created_date=workout_json["createdDate"]
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

    workout_session = WorkoutSession.objects.get(id=wsID)
    ws_dict = {"id": workout_session.id,
               "workoutID": workout_session.workout_id_id,
               "userID": workout_session.user_id_id,
               "startTime": workout_session.start_time,
               "endTime": workout_session.end_time,
               "caloriesBurned": workout_session.calories
               }
    json_string = json.dumps(ws_dict)
    return HttpResponse(json_string)


@api_view(['POST'])
def getWorkout(request):
    wID = json.loads(request.body.decode("utf_8"))

    # Workout
    # {
    # id: String
    # creatorID: String
    #
    # createdDate: Double // dates are stored as doubles
    # title: String
    # caption: String
    # category: String
    # }

    workout = Workout.objects.get(id=wID)
    workout_dict = {"id": workout.id, "creatorID": workout.creator_id_id,
                    "title": workout.title, "caption": workout.caption,
                    "createdDate": workout.created_date, "category": workout.category
                    }

    json_string = json.dumps(workout_dict)
    return HttpResponse(json_string)


@api_view(['POST'])
def postVideo(request):
    js_workout_vid = json.loads(request.body)
    filename = js_workout_vid["workoutID"]
    binary_data = js_workout_vid["videoData"]
    new_file = open(videos_path + filename, 'w')
    new_file.write(binary_data)
    new_file.close()

    # add below when front end starts checking responses
    # worked = True
    # try:
    #     r = open(path_name + filename, 'r')
    # except IOError:
    #     worked = False
    #
    # if worked:
    #     return HttpResponse("True")
    # else:
    #     return HttpResponse("False")

    return HttpResponse()


@api_view(['POST'])
def downloadVideo(request):
    file_name = json.loads(request.body)
    new_file = open(videos_path + file_name, 'r')
    binary_data = new_file.read()
    new_file.close()

    return HttpResponse(binary_data)

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

# @api_view(['POST'])
# def saveWorkout(request):
#     # assume workout Id and User ID passed in
#     json_Workout = json.loads(request.body.decode("utf_8"))
#     userId = json_Workout["userID"]
#     wID = json_Workout["workoutID"]
#     newWorkout = SavedWorkout.create(saver_id = userId, workout_id = wID)
#     newWorkout.save()
#     return HttpResponse("Success")