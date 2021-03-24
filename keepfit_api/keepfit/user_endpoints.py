from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db import models
from .s import *
from .user import User
from .user import following
from .user import Workout
from .user import WorkoutSession
from django.core.files import File

import base64
import os
import json

def update_user(request):
    user_info = json.loads(request.body.decode("utf_8"))
    user_id = user_info["id"]
    user = User.objects.filter(id = user_id)
    user.height_in_inches = user_info["inches"]
    user.sex = user_info["sex"]
    user.profilePicture = user_login["profilePicture"]
    user.username = user_info["username"]
    user.bio = user_info["shortBiography"]
    user.save()
    return Response("Updated")
    #
    # sending new_user object same ID as existing user
    # reassign everythin but password
    # create user from new info
    # update
    #


def reset_password(request):
    pass

def follow_user(request):
    follow_json = json.loads(request.body.decode("utf_8"))
    follower = follow_json["followerID"] # username of the person following someone
    following = follow_json["followingID"] # person they want to follow
    user = User.objects.filter(user_name = follower)
    user2 = User.objects.filter(user_name= following)
    f = following(follower = user, following = user2)
    f.save()
    if(len(following.objects.filter(user_name = follower)) > 0
            and len(following.objects.filter(user_name = following)) > 0):
        return Response("Success")
    else:
        return Response("Failure")
def get_user_preview(request):
    user_info = json.loads(request.body.decode("utf_8"))

    user_id = user_info["id"]
    user = User.objects.filter(id=user_id)
    user_name = user.username
    bio = user.bio
    pic = user.profilePicture
    published_workouts = list(Workout.objects.filter(user__creater_id = user_id ))
    sessionIDs = list(WorkoutSession.objects.filter(user__user_id = user_id))
    items = { "id":user_id, "user_name ": user_name, "shortBiography":bio,
              "profilePicture":pic,"sessionIDs":sessionIDs ,"publishedWorkoutIDs":published_workouts}
    json_string = json.dumps(items)
    return Response(json_string)

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


    pass
def get_followings(request): # pass in user name
    follow_json = json.loads(request.body.decode("utf_8")) # to get who is a
    follower = follow_json[0]           #user is following
    people_following = following.models.filter(user__username = follower)
    listOfDictionaries = [ob.__dict__ for ob in people_following]
    json_string = json.dumps(listOfDictionaries)
    return Response(json_string)

def retrieve_user_profile_pic(request):
    pass

# Create your views here.
@api_view(['POST'])
def user_login(request):
    # User
    # {
    #     "id": String,
    #     "inches": Integer,
    #     "sex": String,
    #     "profilePicture": String,
    #     "password": String,
    #     "likedWorkoutIDs": [String],
    #     "publishedWorkoutIDs": [String],
    #     "pounds": Int
    #     "username": String,
    #     "followingIDs": [String],
    #     "sessionIDs": [String],
    #     "shortBiography": String
    # }

    login_json = json.loads(request.body.decode("utf_8"))

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
            user_id = user.id
            user_name = user.username
            bio = user.bio
            pic = user.profilePicture
            published_workouts = list(Workout.objects.filter(user__creater_id=user_id))
            sessionIDs = list(WorkoutSession.objects.filter(user__user_id=user_id))
            items = {"id": user_id, "user_name ": user_name, "shortBiography": bio,
                     "profilePicture": pic, "sessionIDs": sessionIDs, "publishedWorkoutIDs": published_workouts}
            json_string = json.dumps(items)
            return Response(json_string)
        else:
            return Response("badpassword")
    # Else the username doesn't exist
    else:
        return Response("badusername")


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
        n = text_file.write(profile)
        text_file.close()
        new_user = User.objects.create(
            id=new_user_json["id"],
            sex=new_user_json["sex"],
            weight=new_user_json["pounds"],
            height_in_inches=new_user_json["inches"],
            bio = new_user_json["shortBiography"],
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

        return Response("Success")
    else:
        return Response("Failure")

