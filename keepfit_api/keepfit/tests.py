
from django.test import TestCase
from .user import *
# from django.shortcuts import render
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from django.db import models
# from .s import *
# from .user import *
# from django.core.files import File
# from django.http import HttpRequest
# from .user_endpoints import photos_path
# from .user import *
# from .user_endpoints import *
# from .workout_endpoints import *
# from .search_endpoints import *
from .endpoints_for_testing import *

#1
class UserCreatedSuccesfully(TestCase):
    def setUp(self):
        items = {"id":"jasonGomez",
        "sex":"Male",
        "pounds":542,
        "inches":39,
        "shortBiography":"Insert Bio here",
        "birthdate":300.23,
        "username":"username",
        "password":"password"}
        result = create_user(items)

    def test_createUserVerify(self):
        # to verify that we are correctly making users
        user = User.objects.filter(username="username")
        self.assertEqual(1, len(user))


    def test_createrUser_duplicateUsername(self):

        items = {"id": "jasonGomez",
                 "sex": "Male",
                 "pounds": 542,
                 "inches": 39,
                 "shortBiography": "Insert Bio here",
                 "birthdate": 300.23,
                 "username": "username",
                 "password": "password"}
        result = create_user(items)
        if(result == "Duplicate"):
            assert ("Duplicate Username")

    def test_updateUser(self):
        items = {"id": "tenp",
                 "sex": "Male",
                 "pounds": 542,
                 "inches": 39,
                 "shortBiography": "Insert Bio here",
                 "birthdate": 300.23,
                 "username": "jasong1278",
                 "password": "password"}
        result = create_user(items)
        items1 = {"id": "tenp",
                 "sex": "Female",
                 "pounds": 100,
                 "inches": 100,
                 "shortBiography": "New Bio",
                 "birthdate": 1.01,
                 "username": "jasong1278",
                 "password": "password"}
        update_user(items1)

        u = User.objects.filter(username="jasong1278")
        user = u[0]
        self.assertEqual(100, user.weight)
        self.assertEqual(100, user.height_in_inches)
        self.assertEqual("New Bio", user.bio)
        self.assertEqual(1.01, user.birthday)

class LoginTestings(TestCase):
    def setUp(self):
        items = {"id": "jasonGomez",
                 "sex": "Male",
                 "pounds": 542,
                 "inches": 39,
                 "shortBiography": "Insert Bio here",
                 "birthdate": 300.23,
                 "username": "username",
                 "password": "password"}
        result = create_user(items)
    def test_loginTest(self):
        result = user_login({"username":"username" , "password":"password"})
        self.assertEqual("Success", result)
    def test_login_badusername(self):
        result = user_login({"username": "WOOOOOW", "password": "password"})
        self.assertEqual("badusername", result)
    def test_login_password(self):
        result = user_login({"username": "username", "password": "bitch"})
        self.assertEqual("badpassword", result)
#2
class WorkoutCreatedSuccessfully(TestCase):
    def setUp(self):
        items = {"id": "jasonGomez",
                 "sex": "Male",
                 "pounds": 542,
                 "inches": 39,
                 "shortBiography": "Insert Bio here",
                 "birthdate": 300.23,
                 "username": "username",
                 "password": "password"}
        result = create_user(items)
        items2 = {
            "id": "arg",
            "title": "TEMP WORKOUT" ,
            "creatorID": "jasonGomez" ,
            "caption" : "workout fun",
            "category" : "HIIT",
            "createdDate": 800.23
        }
        publishWorkout(items2)
    def test_createWorkout(self):
        workout = Workout.objects.filter(id="arg")
        self.assertEqual(1, len(workout))

#3
class WorkoutSessionCreatedSuccessfully(TestCase):
    def setUp(self):
        items = {"id": "jasonGomez",
                 "sex": "Male",
                 "pounds": 542,
                 "inches": 39,
                 "shortBiography": "Insert Bio here",
                 "birthdate": 300.23,
                 "username": "username",
                 "password": "password"}
        result = create_user(items)
        items2 = {
            "id": "arg",
            "title": "TEMP WORKOUT",
            "creatorID": "jasonGomez",
            "caption": "workout fun",
            "category": "HIIT",
            "createdDate": 800.23
        }
        result2 = publishWorkout(items2)
        items3 = {
            "id": "ws",
            "workoutID": "arg",
            "caloriesBurned": 100,
            "userID": "jasonGomez",
            "startTime": 30.00,
            "endTime": 88.00
        }
        result3 = completeWorkout(items3)
    def test_createWS(self):

        workout_s = WorkoutSession.objects.filter(id="ws")
        self.assertEqual(1, len(workout_s))
#4
class UsersFoundSuccesfully(TestCase): #this is testing the searchUsers endpoint
    def setUp(self):
        pass
    def test_usersfoundsuccesfully(self):

        item1 = {"id": "jasonGomez2",
                  "sex": "Male",
                  "pounds": 542,
                  "inches": 39,
                  "shortBiography": "Insert Bio here",
                  "birthdate": 300.23,
                  "username": "jason1",
                  "password": "password"}
        item2 = {"id": "jasonGomez9",
                 "sex": "Male",
                 "pounds": 542,
                 "inches": 39,
                 "shortBiography": "Insert Bio here",
                 "birthdate": 300.23,
                 "username": "jason2",
                 "password": "password"}
        item3 = {"id": "jasonGomez3",
                 "sex": "Male",
                 "pounds": 542,
                 "inches": 39,
                 "shortBiography": "Insert Bio here",
                 "birthdate": 300.23,
                 "username": "jason3",
                 "password": "password"}
        item4 = {"id": "jasonGomez4",
                 "sex": "Male",
                 "pounds": 542,
                 "inches": 39,
                 "shortBiography": "Insert Bio here",
                 "birthdate": 300.23,
                 "username": "jason4",
                 "password": "password"}
        create_user(item1)
        create_user(item2)
        create_user(item3)
        create_user(item4)
        users = searchUsers("jason")
        self.assertEqual(4, len(users))


#5
class FollowSuccess(TestCase): #tests if a user can follow another user
    def setUp(self):

        item1 = {"id": "jasonGomez1",
                 "sex": "Male",
                 "pounds": 542,
                 "inches": 39,
                 "shortBiography": "Insert Bio here",
                 "birthdate": 300.23,
                 "username": "jason1",
                 "password": "password"}
        item2 = {"id": "jasonGomez2",
                 "sex": "Male",
                 "pounds": 542,
                 "inches": 39,
                 "shortBiography": "Insert Bio here",
                 "birthdate": 300.23,
                 "username": "jason2",
                 "password": "password"}
        create_user(item1)
        create_user(item2)
        follow_user({"followerID": "jasonGomez1", "followingID": "jasonGomez2"})

    def test_followsuccess(self):
        followIDs = Following.objects.filter(follower__id="jasonGomez1").values("following__id").values_list(
            'following__id', flat=True)
        self.assertEqual(1, len(followIDs))
class UnFollowSuccess(TestCase):
    def setUp(self):
        item1 = {"id": "jasonGomez1",
                 "sex": "Male",
                 "pounds": 542,
                 "inches": 39,
                 "shortBiography": "Insert Bio here",
                 "birthdate": 300.23,
                 "username": "jason1",
                 "password": "password"}
        item2 = {"id": "jasonGomez2",
                 "sex": "Male",
                 "pounds": 542,
                 "inches": 39,
                 "shortBiography": "Insert Bio here",
                 "birthdate": 300.23,
                 "username": "jason2",
                 "password": "password"}
        create_user(item1)
        create_user(item2)
        follow_user({"followerID": "jasonGomez1", "followingID": "jasonGomez2"})
        unfollow_user({"followerID": "jasonGomez1", "followingID": "jasonGomez2"})
    def test_unfollow(self):
        followIDs = Following.objects.filter(follower__id="jasonGomez1").values("following__id").values_list(
            'following__id', flat=True)
        self.assertEqual(0, len(followIDs))
#7
class LikeWorkout(TestCase): #tests if one can like a workout
    def setUp(self):
        items = {"id": "jasonGomez",
                 "sex": "Male",
                 "pounds": 542,
                 "inches": 39,
                 "shortBiography": "Insert Bio here",
                 "birthdate": 300.23,
                 "username": "username",
                 "password": "password"}
        result = create_user(items)
        items_= {"id": "sam",
                 "sex": "Male",
                 "pounds": 54,
                 "inches": 339,
                 "shortBiography": " Bio here",
                 "birthdate": 30.23,
                 "username": "arnold",
                 "password": "pass"}
        result_ = create_user(items_)
        items2 = {
            "id": "arg",
            "title": "TEMP WORKOUT",
            "creatorID": "sam",
            "caption": "workout fun",
            "category": "HIIT",
            "createdDate": 800.23
        }
        publishWorkout(items2)


        list = {
            "userID" : "jasonGomez",
            "workoutID" : "arg"
        }
        likeWorkout(list)

    def test_likeWK(self):
        likedWorkoutIDs = list(
            LikedWorkout.objects.filter(liker_id__id="jasonGomez").values_list('workout_id__id', flat=True))
        self.assertEqual(1, len(likedWorkoutIDs))
    def test_unlike(self):
        list2 = {
            "userID": "jasonGomez",
            "workoutID": "arg"
        }
        unlikeWorkout(list2)
        likedWorkoutIDs = list(
            LikedWorkout.objects.filter(liker_id__id="jasonGomez").values_list('workout_id__id', flat=True))
        self.assertEqual(0, len(likedWorkoutIDs))

# #9
# class searchForCategory(TestCase): #tests if one can search for a post with a category
#     def setUpClass(self):
#         pass
#     def test_sfc(self):
#         pass
#
# #10
# class searchForEmptyListOfCategories(TestCase): #searching for an empty category should return an empty list
#     def setUpClass(self):
#         pass
#     def test_emptylist(self):
#         pass

#11
class searchForWorkout(TestCase): #searching for a workout not made should not return a valid workout
    def setUp(self):
        items = {"id": "jasonGomez",
                 "sex": "Male",
                 "pounds": 542,
                 "inches": 39,
                 "shortBiography": "Insert Bio here",
                 "birthdate": 300.23,
                 "username": "username",
                 "password": "password"}
        result = create_user(items)
        items2 = {
            "id": "arg",
            "title": "TEMP WORKOUT",
            "creatorID": "jasonGomez",
            "caption": "workout fun",
            "category": "HIIT",
            "createdDate": 800.23
        }
        publishWorkout(items2)

    def test_unmadeWorkout(self):
        list_ = list(Workout.objects.filter(creator_id__id="H").values_list('id', flat=True))
        self.assertEqual(0,len(list_))
    def test_madeWorkout(self):
        list_ =list(Workout.objects.filter(creator_id__id="jasonGomez").values_list('id', flat=True))
        self.assertEqual(1,len(list_))
    def test_empty_workoutSessions(self): #new user should have no workoutsessions
        sessionIDs = list(WorkoutSession.objects.filter(user_id__id="jasonGomez").values_list('id', flat=True))
        self.assertEqual(0,len(sessionIDs))


#12
class searchForUser(TestCase):
    def setUp(self):
        item1 = {"id": "jasonGomez2",
                 "sex": "Male",
                 "pounds": 542,
                 "inches": 39,
                 "shortBiography": "Insert Bio here",
                 "birthdate": 300.23,
                 "username": "jason1",
                 "password": "password"}
        create_user(item1)
    def test_unmadeUser(self):
        list_ = searchUsers("Dana")
        self.assertEqual(0,len(list_))
    def test_madeUser(self):
        list_ = searchUsers("jason1")
        self.assertEqual(1,len(list_))

