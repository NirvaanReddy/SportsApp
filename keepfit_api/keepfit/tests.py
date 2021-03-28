
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


class UserCreatedSuccesfully(TestCase):

    def setUp(self):
        items = {"id":"jasonGomez",
        "sex":"Male",
        "pounds":542,
        "height_in_inches":39,
        "bio":"Insert Bio here",
        "birthdate":300.23,
        "username":"username",
        "password":"password"}
        create_user(items)

    def test_createUserVerify(self):
        # to verify that we are correctly making users
        user = User.objects.filter(username="username")
        self.assertEqual(1, len(user))
        print()


class WorkoutCreatedSuccessfully(TestCase):
    def setUp(self):
        pass
    def test_createWorkout(self):
        pass

class WorkoutSessionCreatedSuccessfully(TestCase):
    def setUpClass(self):
        pass
    def test_createWS(self):
        pass

#