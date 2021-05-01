from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db import models
from .s import *
from .user import *
from django.core.files import File
from django.http import HttpResponse
from collections import Counter

import base64
import os
import json


videos_path = "/Users/samdonovan/Desktop/TempVids/" if testing else "/home/ec2-user/videos/"
# videos_path = "/home/ec2-user/videos/"

def getNumberLikes(workout):
    return LikedWorkout.objects.filter(workout_id_id = workout.id).count()

@api_view(['POST'])
def getMostLikedWorkoutOfCategory(request):
    categoryString = json.loads(request.body.decode("utf_8"))
    workoutsOfCategory = list(Workout.objects.filter(category=categoryString))
    if len(workoutsOfCategory) == 0:
        return HttpResponse("null")
    max = -1
    best = None
    for workout in workoutsOfCategory:
        currentLikes = getNumberLikes(workout)
        if currentLikes > max:
            max = currentLikes
            best = workout
    return HttpResponse(json.dumps(best.id))

@api_view(['POST'])
def publishWorkoutPlan(request):
    json_Workout = json.loads(request.body.decode("utf_8"))
    id = json_Workout["id"]
    user_id = json_Workout["userID"]
    wID = json_Workout["workoutID"]
    data = float(json_Workout["date"])
    new_workout = PlannedWorkout.objects.create(id = id, planner_id_id = user_id, workout_id_id= wID, date = data)
    new_workout.save()
    return HttpResponse("Success")


@api_view(['POST'])
def publishComment(request):
    new_comment_json = json.loads(request.body.decode("utf_8"))
    username_id = new_comment_json["userID"]
    wID = new_comment_json["workoutID"]
    comment = new_comment_json["comment"]
    id = new_comment_json["id"]
    new_comment = Comments.objects.create(id = id, user_id = username_id, workout_id = wID, comment = comment)
    new_comment.save()
    return HttpResponse("Success")

@api_view(['POST'])
def deleteWorkoutPlan(request):
    id = json.loads(request.body.decode("utf_8"))
    w = PlannedWorkout.objects.get(id=id)
    w.delete()
    return HttpResponse("Success")


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
        created_date=workout_json["createdDate"],
        comment_status=workout_json["commentsEnabled"]
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
def returnCommentStatus(request):
    wID = json.loads(request.body.decode("utf_8"))
    workout = Workout.objects.get(id=wID)
    c_status = workout.comment_status
    json_string = json.dumps(c_status)
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
    comments = Comments.objects.filter(workout_id = workout.id)
    commentsDict = map(lambda comment: {
        "id": comment.id,
        "userID": comment.user_id,
        "comment": comment.comment,
        "workoutID": comment.workout_id
    }, comments)
    workout_dict = {"id": workout.id, "creatorID": workout.creator_id_id,
                    "title": workout.title, "caption": workout.caption,
                    "createdDate": workout.created_date, "category": workout.category,
                    "comments": list(commentsDict), "commentsEnabled": workout.comment_status
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


@api_view(['POST'])
def get10MostLikedWorkouts(request):
    words = LikedWorkout.objects.all().values_list('workout_id', flat=True)
    most_common_words = [word for word, word_count in Counter(words).most_common(10)]
    print(most_common_words)
    json_string = json.dumps(most_common_words)
    return HttpResponse(json_string)

@api_view(['POST'])
def get10MostLikedWorkoutsOfCategory(request):
    category_name = json.loads(request.body)
    words = LikedWorkout.objects.filter(category=category_name).values_list('workout_id', flat = True)
    most_common_words = [word for word, word_count in Counter(words).most_common(10)]
    json_strong = json.dumps(most_common_words)
    return HttpResponse(json_strong)