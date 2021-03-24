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

def update_user(request):
    user_info = json.loads(request.body.decode("utf_8"))
    user_id = user_info["id"]
    user = User.objects.filter(id = user_id)
    user.height_in_inches = user_info["inches"]
    user.sex = user_info["sex"]
    # user.profilePicture = user_login["profilePictu

    # save profile picture
    profile = user_info["profilePicture"]
    text_file = open("/home/ec2-user/photos/" + user_info["id"], "w")
    text_file.write(profile)
    text_file.close()

    user.username = user_info["username"]
    user.bio = user_info["shortBiography"]

    user.save()



    return HttpResponse("Updated")
    #
    # sending new_user object same ID as existing user
    # reassign everythin but password
    # create user from new info
    # update
    #


def reset_password(request):
    user_info = json.loads(request.body.decode("utf_8"))
    username =  user_info["username"]
    old_password = user_info["old_password"]
    new_password = user_info["new_password"]
    users = User.objects.filter(username=username)
    if(len(users) == 1):
        user = users[0]
        if(old_password == user.password):
            user.password = new_password
            return HttpResponse("Success")
        else:
            return HttpResponse("notmatching")


def follow_user(request):
    follow_json = json.loads(request.body.decode("utf_8"))
    follower = follow_json["followerID"] # username of the person following someone
    following = follow_json["followingID"] # person they want to follow
    user = User.objects.filter(username = follower)
    user2 = User.objects.filter(username= following)
    f = Following(follower = user, following = user2)
    f.save()
    if(len(Following.objects.filter(username = follower)) > 0
            and len(Following.objects.filter(username = following)) > 0):
        return HttpResponse("Success")
    else:
        return HttpResponse("Failure")

def get_followers(username): # pass in user name
    people_followers = User.models.filter(followings__follower = username).values("id")
    # answers.values_list('id', flat=True)

    follower_ids = people_followers.values_list('id', flat= True)
    return follower_ids
def get_followings(username):
    people_following = User.models.filter(followings__following=username).values("id")
    follower_ids = people_following.values_list('id', flat=True)
    return follower_ids

def get_user_preview(request):
    user_id = json.loads(request.body.decode("utf_8"))

    text_file = open("/home/ec2-user/photos/" + user_id, "r")
    pic = text_file.read()
    text_file.close()

    user = User.objects.filter(id=user_id)
    user_name = user.username
    bio = user.bio
    published_workouts = Workout.objects.filter(user__creator_id=user_id).values("id").values_list('id', flat = True)
    sessionIDs = WorkoutSession.objects.filter(user__user_id=user_id).values("id").values_list('id', flat = True)
    followers = get_followers(user_name)
    followings = get_followings(user_name)

    # liked == [String] where each string is an id of a workout the user liked
    likedWorkouts = Workout.objects.filter(liked_workouts__liker_id=user.id).values("id").values_list('id', flat = True)
    items = { "id":user_id, "username ": user_name, "shortBiography":bio,
              "profilePicture":pic, "followers": followers,"followings":followings ,
              "sessionIDs":sessionIDs ,"publishedWorkoutIDs":published_workouts,
              "likedWorkoutIDs":likedWorkouts}
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

# Create your views here.
@api_view(['POST'])
def user_login(request):
    login_json = json.loads(request.body.decode("utf_8"))
    print(login_json)

    username = login_json["username"]
    password = login_json["password"]

    users = User.objects.filter(username=username)
    # If the username exists
    # people I'm following
    #people who follow me
    if len(users) == 1:
        user = users[0]
        # If the password matches
        if password == user.password:

            text_file = open("/home/ec2-user/photos/" + user.id, "r")
            pic = text_file.read()
            text_file.close()

            user_id = user.id
            user_name = user.username
            bio = user.bio
            published_workouts = Workout.objects.filter(creator_id=user_id).values("id").values_list('id', flat = True)

            sessionIDs = WorkoutSession.objects.filter(user_id=user_id).values("id").values_list('id', flat = True)

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

            items = {"id": user_id, "username ": user_name, "shortBiography": bio,
                     "profilePicture": pic, "sessionIDs": sessionIDs, "publishedWorkoutIDs": published_workouts}
            print (items + " <--items")
            json_string = json.dumps(items)
            return HttpResponse(json_string)
        else:
            return HttpResponse("badpassword")
    # Else the username doesn't exist
    else:
        return HttpResponse("badusername")


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
        text_file = open("/home/ec2-user/photos/" + new_user_json["id"], "w")
        text_file.write(profile)
        text_file.close()
        new_user = User.objects.create(
            id=new_user_json["id"],
            sex=new_user_json["sex"],
            weight=new_user_json["pounds"],
            height_in_inches=new_user_json["inches"],
            bio=new_user_json["shortBiography"],
            username=new_user_json["username"],
            password=new_user_json["password"],
            #birth_date=new_user_json["birth_date"]
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

