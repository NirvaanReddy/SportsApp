
from django.test import TestCase
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db import models
from .s import *
from .user import *
from django.core.files import File
from django.http import HttpRequest
from .user_endpoints import photos_path
from .user import *
from .user_endpoints import *
from .workout_endpoints import *
from .search_endpoints import *


class UserCreatedSuccesfully(TestCase):

    def setUp(self):
        pass
    def test_createUserVerify(self):
        # to verify that we are correctly making users
        items = { "id": "whatever" ,"sex": "Male", "pounds":170,
                  "inches": 170, "shortBiography": "My name is Jason Gomez :)",
                  "birthdate" : 2.3 , "username" : "jjjj" , "password": "stringstring"
                  }
        json_string = json.dumps(items)
        result = create_user(HttpRequest(json_string))

        self.assertEqual("Hello", 'The lion says "roar"')
