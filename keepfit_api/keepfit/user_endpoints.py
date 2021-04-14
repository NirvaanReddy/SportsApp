from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db import models
from .s import *
from .user import User
from .user import Following
from .user import Workout
from .user import WorkoutSession
from .workout_endpoints import *
from django.core.files import File
from django.http import HttpResponse

import base64
import os
import json

# photos_path = "~/Desktop/TempPics/"
photos_path = "/home/ec2-user/photos/"

# sends user object which overwrites the user with the same ID
# reassign everything but password
@api_view(['POST'])
def update_user(request):
    user_info = json.loads(request.body.decode("utf_8"))
    user_id = user_info["id"]
    user = User.objects.get(id=user_id)

    check_username = user_info["username"]
    should_be_empty = User.objects.filter(username=check_username)
    if (len(should_be_empty) != 0):
        return HttpResponse("That username already exists")

    user.username = user_info["username"]
    user.bio = user_info["shortBiography"]
    user.weight = user_info["pounds"]
    user.height_in_inches = user_info["inches"]
    user.sex = user_info["sex"]
    user.birthday = user_info["birthdate"]

    # save profile picture
    profile = user_info["profilePicture"]
    text_file = open(photos_path + user_info["id"], "w")
    text_file.write(profile)
    text_file.close()

    user.save()

    return HttpResponse("Updated")



@api_view(['POST'])
def reset_password(request):
    user_info = json.loads(request.body.decode("utf_8"))
    id = user_info["id"]
    old_password = user_info["oldPassword"]
    new_password = user_info["newPassword"]
    users = User.objects.filter(id=id)
    if (len(users) == 1):
        user = users[0]
        if (old_password == user.password):
            user.password = new_password
            user.save()
            return HttpResponse("true")
    return HttpResponse("false")


@api_view(['POST'])
def follow_user(request):
    follow_json = json.loads(request.body.decode("utf_8"))
    follower = follow_json["followerID"]  # username of the person following someone
    following = follow_json["followingID"]  # person they want to follow

    user = User.objects.get(id=follower)
    user2 = User.objects.get(id=following)

    f = Following.objects.create(follower_id=follower, following_id=following)
    f.save()

    # add below code back when front end start's checking responses
    # if (len(Following.objects.filter(username=follower)) > 0
    #         and len(Following.objects.filter(username=following)) > 0):
    #     return HttpResponse("Success")
    # else:
    #     return HttpResponse("Failure")
    return HttpResponse()

@api_view(['POST'])
def unfollow_user(request):
    follow_json = json.loads(request.body.decode("utf_8"))
    follower = follow_json["followerID"]  # username of the person following someone
    following = follow_json["followingID"]  # person they want to follow

    f = Following.objects.get(follower_id=follower, following_id=following)
    f.delete()

    # add below code back when front end start's checking responses
    # if (len(Following.objects.filter(username=follower)) > 0
    #         and len(Following.objects.filter(username=following)) > 0):
    #     return HttpResponse("Success")
    # else:
    #     return HttpResponse("Failure")
    return HttpResponse()
#
# @api_view(['POST'])
# def get_followers(username): # pass in user name
#     people_followers = User.models.filter(followings__follower = username).values("id")
#     # answers.values_list('id', flat=True)
#
#     follower_ids = people_followers.values_list('id', flat= True)
#     return follower_ids
#
# @api_view(['POST'])
# def get_followings(username):
#     people_following = User.models.filter(followings__following=username).values("id")
#     follower_ids = people_following.values_list('id', flat=True)
#     return follower_ids

# gets a user preview
@api_view(['POST'])
def get_user_preview(request):
    user_id = json.loads(request.body.decode("utf_8"))

    text_file = open(photos_path + user_id, "r")
    pic = text_file.read()
    text_file.close()

    user = User.objects.get(id=user_id)

    # followers = get_followers(user_name)
    # followings = get_followings(user_name)

    sessionIDs = list(WorkoutSession.objects.filter(user_id__id=user_id).values_list('id', flat=True))
    publishedWorkoutIDs = list(Workout.objects.filter(creator_id__id=user_id).values_list('id', flat=True))

    # liked == [String] where each string is an id of a workout the user liked
    likedWorkouts = list(LikedWorkout.objects.filter(liker_id__id=user_id).values_list('workout_id__id', flat=True))

    items = {"id": user_id,
             "username": user.username,
             "shortBiography": user.bio,
             "profilePicture": pic,
             "sessionIDs": sessionIDs,
             "publishedWorkoutIDs": publishedWorkoutIDs,
             "likedWorkoutIDs": likedWorkouts
             }
    json_string = json.dumps(items)
    return HttpResponse(json_string)

    # assuming userID
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


# takes in username/password, sends back user
@api_view(['POST'])
def user_login(request):
    login_json = json.loads(request.body.decode("utf_8"))
    # print(login_json)

    username = login_json["username"]
    password = login_json["password"]

    users = User.objects.filter(username=username)
    # If the username exists
    # people I'm following
    # people who follow me
    if len(users) == 1:
        user = users[0]
        # If the password matches
        if password == user.password:

            text_file = open(photos_path + user.id, "r")
            pic = text_file.read()
            text_file.close()

            user_id = user.id
            user_name = user.username
            bio = user.bio
            bday = user.birthday
            published_workouts = list(Workout.objects.filter(creator_id__id=user_id).values_list('id', flat=True))
            likedWorkoutIDs = list(
                LikedWorkout.objects.filter(liker_id__id=user_id).values_list('workout_id__id', flat=True))
            followIDs = Following.objects.filter(follower__id=user_id).values("following__id").values_list(
                'following__id', flat=True)
            sessionIDs = list(WorkoutSession.objects.filter(user_id__id=user_id).values_list('id', flat=True))
            planned_workouts = list(PlannedWorkout.objects.filter(planner_id__id = user_id).values_list('id', flat=True))
            print(likedWorkoutIDs)

            # User
            # {
            #     "id": String,
            #     "inches": Integer,
            #     "sex": String,
            #     "profilePicture": String,
            #     "password": String,
            #     "pounds": Int
            #     "username": String,
            #     "shortBiography": String
            #     "likedWorkoutIDs": [String],
            #     "publishedWorkoutIDs": [String],
            #     "followingIDs": [String],
            #     "sessionIDs": [String],
            # }

            results = list(SearchHistory.Objects.filter(user_id=user_id).values_list('searchItem', flat=True))
            ten = results[-10:]
            items = {"id": user_id,
                     "username": user_name,
                     "shortBiography": bio,
                     "profilePicture": pic,
                     "sessionIDs": list(sessionIDs),
                     "publishedWorkoutIDs": list(published_workouts),
                     "likedWorkoutIDs": list(likedWorkoutIDs),
                     "sex": user.sex,
                     "birthdate": bday,
                     "followingIDs": list(followIDs),
                     "plannedWorkouts": planned_workouts,
                     "pounds": user.weight,
                     "inches": user.height_in_inches,
                     "10_searches": ten
                     }
            json_string = json.dumps(items)
            return HttpResponse(json_string)
        else:
            return HttpResponse("badpassword")
    # Else the username doesn't exist
    else:
        return HttpResponse("badusername")

@api_view(['POST'])
def deleteWorkoutSession(request):
    ws_id = json.loads(request.body.decode("utf_8")) #assumes I am getting the correct WS id
    WorkoutSession.objects.filter(id=ws_id).delete()
    return HttpResponse("success")

@api_view(["POST"])
def deleteWorkout(request):
    workout_id = json.loads(request.body.decode("utf_8")) #assumes I am getting the correct Workout id
    Workout.objects.filter(id=workout_id).delete()
    return HttpResponse("success")

@api_view(['POST'])
def deleteAccount(request):
    user_id = json.loads(request.body.decode("utf_8"))
    User.objects.filter(id=user_id).delete()
    return HttpResponse("success")

@api_view(['POST'])
def create_user(request):
    new_user_json = json.loads(request.body.decode("utf_8"))
    # serializer = UserSerializer(data=userJson)
    # if not serializer.is_valid():
    #     print("Bad JSON from front end")
    # If the set is empty, create the user and the profile picture
    query_results = User.objects.filter(username=new_user_json["username"])
    if len(query_results) == 0:
        profile = new_user_json["profilePicture"]
        text_file = open(photos_path + new_user_json["id"], "w")
        text_file.write(profile)
        text_file.close()
        new_user = User.objects.create(
            id=new_user_json["id"],
            sex=new_user_json["sex"],
            weight=new_user_json["pounds"],
            height_in_inches=new_user_json["inches"],
            bio=new_user_json["shortBiography"],
            birthday=new_user_json["birthdate"],
            username=new_user_json["username"],
            password=new_user_json["password"],
        )
        new_user.save()

        # Create the profile picture
        # _id = new_user.pk
        # image_data = base64.b64decode(profile_pic_data)
        # file_name = str(new_user_id) + "profile_pic.jpg"
        # with open(file_name, 'wb+') as f:
        #     new_image = File(f)
        #     new_image.write(image_data)
        #     user.profile_picture = new_image
        #     user.save()

        return HttpResponse("true")
    else:
        return HttpResponse("false")

