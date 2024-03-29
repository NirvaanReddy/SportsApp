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

# sends user object which overwrites the user with the same ID
# reassign everything but password

def update_user(user_info):
    user_id = user_info["id"]
    user = User.objects.get(id=user_id)

    user.username = user_info["username"]

    user.bio = user_info["shortBiography"]
    user.weight = user_info["pounds"]
    user.height_in_inches = user_info["inches"]
    user.sex = user_info["sex"]
    user.birthday = user_info["birthdate"]

    # save profile picture
    # profile = user_info["profilePicture"]
    # text_file = open(photos_path + user_info["id"], "w")
    # text_file.write(profile)
    # text_file.close()

    user.save()

    return HttpResponse("Updated")



def reset_password(user_info):
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


def follow_user(follow_json):
   # follow_json = json.loads(request.body.decode("utf_8"))
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


def unfollow_user(follow_json):
    #follow_json = json.loads(request.body.decode("utf_8"))
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
# @api_view(['POST'])
# def get_user_preview(request):
#     user_id = json.loads(request.body.decode("utf_8"))
#
#     text_file = open(photos_path + user_id, "r")
#     pic = text_file.read()
#     text_file.close()
#
#     user = User.objects.get(id=user_id)
#
#     # followers = get_followers(user_name)
#     # followings = get_followings(user_name)
#
#     sessionIDs = list(WorkoutSession.objects.filter(user_id__id=user_id).values_list('id', flat=True))
#     publishedWorkoutIDs = list(Workout.objects.filter(creator_id__id=user_id).values_list('id', flat=True))
#
#     # liked == [String] where each string is an id of a workout the user liked
#     likedWorkouts = list(LikedWorkout.objects.filter(liker_id__id=user_id).values_list('workout_id__id', flat=True))
#
#     items = {"id": user_id,
#              "username": user.username,
#              "shortBiography": user.bio,
#              "profilePicture": pic,
#              "sessionIDs": sessionIDs,
#              "publishedWorkoutIDs": publishedWorkoutIDs,
#              "likedWorkoutIDs": likedWorkouts
#              }
#     json_string = json.dumps(items)
#     return HttpResponse(json_string)

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

def user_login(login_json):
   # login_json = json.loads(request.body.decode("utf_8"))
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

            # text_file = open(photos_path + user.id, "r")
            # pic = text_file.read()
            # text_file.close()

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

            items = {"id": user_id,
                     "username": user_name,
                     "shortBiography": bio,
                     "sessionIDs": list(sessionIDs),
                     "publishedWorkoutIDs": list(published_workouts),
                     "likedWorkoutIDs": list(likedWorkoutIDs),
                     "sex": user.sex,
                     "birthdate": bday,
                     "followingIDs": list(followIDs),
                     "pounds": user.weight,
                     "inches": user.height_in_inches
                     }


            return "Success"
        else:
            return "badpassword"
    # Else the username doesn't exist
    else:
        return "badusername"



def create_user(new_user_json):
   # new_user_json = json.loads(request.body.decode("utf_8"))
    # serializer = UserSerializer(data=userJson)
    # if not serializer.is_valid():
    #     print("Bad JSON from front end")
    # If the set is empty, create the user and the profile picture
    query_results = User.objects.filter(username=new_user_json["username"])

    if len(query_results) == 0:
        # profile = new_user_json["profilePicture"]
        # text_file = open(photos_path + new_user_json["id"], "w")
        # text_file.write(profile)
        # text_file.close()
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
        return "Success"
    else:
        return "Duplicate"
        # Create the profile picture
        # _id = new_user.pk
        # image_data = base64.b64decode(profile_pic_data)
        # file_name = str(new_user_id) + "profile_pic.jpg"
        # with open(file_name, 'wb+') as f:
        #     new_image = File(f)
        #     new_image.write(image_data)
        #     user.profile_picture = new_image
        #     user.save()





def searchCategory(type):


    categories = Workout.objects.filter(category=type)

    listOfDictionaries = []
    for workout in categories:
        listOfDictionaries.append({"id": workout.id, "creatorID": workout.creator_id_id,
                                   "title": workout.title, "caption": workout.caption,
                                   "createdDate": workout.created_date, "category": workout.category
                                   })


    json_string = json.dumps(listOfDictionaries)

    return HttpResponse(json_string)
    # https://pythonexamples.org/python-list-to-json/#3


def searchUsers(name):

    # name is now a string of the sent username
    users = User.objects.filter(username__startswith=name)

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

    listOfDictionaries = []
    for user in users:
       #
        # pic = text_file.read()
        # text_file.close()

        sessionIDs = list(WorkoutSession.objects.filter(user_id__id=user.id).values_list('id', flat=True))
        publishedWorkoutIDs = list(Workout.objects.filter(creator_id__id=user.id).values_list('id', flat=True))

        # liked == [String] where each string is an id of a workout the user liked
        likedWorkouts = list(LikedWorkout.objects.filter(liker_id__id=user.id).values_list('workout_id__id', flat=True))

        listOfDictionaries.append({"id": user.id,
                                   "username": user.username,
                                   "shortBiography": user.bio,
                                   #"profilePicture": pic,
                                   "sessionIDs": sessionIDs,
                                   "publishedWorkoutIDs": publishedWorkoutIDs,
                                   "likedWorkoutIDs": likedWorkouts
                                   })
    # print(listOfDictionaries)

    return listOfDictionaries



def searchWorkouts(request):
    title_ = json.loads(request.body.decode("utf_8"))

    workouts = Workout.objects.filter(title__startswith=title_)

    listOfDictionaries = []
    for workout in workouts:
        listOfDictionaries.append({"id": workout.id, "creatorID": workout.creator_id_id,
                                   "title": workout.title, "caption": workout.caption,
                                   "createdDate": workout.created_date, "category": workout.category
                                   })


    json_string = json.dumps(listOfDictionaries)

    return HttpResponse(json_string)

videos_path = "/home/ec2-user/videos/"

def likeWorkout(request):
    # assume workout Id and User ID passed in
    json_Workout = request
    userId = json_Workout["userID"]
    wID = json_Workout["workoutID"]
    user = User.objects.get(id=userId)
    workout = Workout.objects.get(id=wID)
    newWorkout = LikedWorkout.objects.create(liker_id=user, workout_id=workout)
    newWorkout.save()


def unlikeWorkout(request):
    # assume workout Id and User ID passed in
    json_Workout = request
    userId = json_Workout["userID"]
    wID = json_Workout["workoutID"]

    oldWorkout = LikedWorkout.objects.get(liker_id_id=userId, workout_id_id=wID)
    oldWorkout.delete()


def completeWorkout(json_Workout):
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

   # json_Workout = json.loads(request.body.decode("utf_8"))

    newWorkout = WorkoutSession.objects.create(id=json_Workout["id"],
                                       workout_id_id=json_Workout["workoutID"],
                                       calories=json_Workout["caloriesBurned"],
                                       user_id_id=json_Workout["userID"],
                                       start_time=json_Workout["startTime"],
                                       end_time=json_Workout["endTime"]
                                       )
    newWorkout.save()



def publishWorkout(workout_json):
    #workout_json = json.loads(request.body.decode("utf_8"))

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



def getWorkoutSession(wsID):
   # wsID = json.loads(request.body.decode("utf_8"))

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


def getWorkout(wID):
   # wID = json.loads(request.body.decode("utf_8"))

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


def postVideo(request):
    js_workout_vid = json.loads(request.body)
    filename = js_workout_vid["workoutID"]
    binary_data = js_workout_vid["videoData"]
    new_file = open(videos_path + filename, 'w')
    new_file.write(binary_data)
    new_file.close()

    return HttpResponse()



def downloadVideo(request):
    file_name = json.loads(request.body)
    new_file = open(videos_path + file_name, 'r')
    binary_data = new_file.read()
    new_file.close()

    return HttpResponse(binary_data)
