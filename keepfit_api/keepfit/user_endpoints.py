from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db import models
from .s import *
from .user import User
from django.core.files import File

import base64
import os
import json

def update_user(request):
    pass

def get_forgot_password_questions(request):
    pass

def reset_password(request):
    pass

def follow_user(request):
    pass

def retrieve_user_profile_pic(request):
    pass

# Create your views here.
@api_view(['POST'])
def user_login(request):

    login_json = json.loads(request.body.decode("utf_8"))

    username = login_json["username"]
    password = login_json["password"]

    users = User.objects.filter(username=username)
    # If the username exists

    if len(users) == 1:
        user = users[0]
        # If the password matches
        if password == user.password:
            return Response(user)
        else:
            return Response("badpassword")
    # Else the username doesn't exist
    else:
        return Response("badusername")


@api_view(['POST'])
def create_user(request):
    new_user_json = request.body.decode("utf_8")

    # serializer = UserSerializer(data=userJson)
    # if not serializer.is_valid():
    #     print("Bad JSON from front end")

    # If the set is empty, create the user and the profile picture
    query_results = User.objects.filter(username=new_user_json["username"])
    if len(query_results) == 0:
        new_user = User.create(
            id=new_user_json["id"],
            profile_picture_url=new_user_json["profile_picture_url"],
            weight=new_user_json["pounds"],
            height_in_inches=new_user_json["height_in_inches"],
            username=new_user_json["username"],
            password=new_user_json["password"],
            birth_date=new_user_json["birth_date"]
        )

        new_user.save()


        # Create the profile picture
        # _id = new_user.pk
        # image_data = base64.b64decode(profile_pic_data)
        # file_name = str(new_user_id) + "profile_pic.jpg"
        #
        # with open(file_name, 'wb+') as f:
        #     new_image = File(f)
        #     new_image.write(image_data)
        #     user.profile_picture = new_image
        #     user.save()

        return Response(new_user.id)
    else:
        return Response("null")

