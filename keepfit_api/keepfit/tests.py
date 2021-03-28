
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
        new_user = User.objects.create(
            id="jasonGomez",
            sex="Male",
            weight=542,
            height_in_inches=39,
            bio="Insert Bio here",
            birthday=300.23,
            username="username",
            password="password",
        )
        new_user.save()

    def test_createUserVerify(self):
        # to verify that we are correctly making users
        user = User.objects.filter(username="jasonGomez")
        self.assertEqual(1, len(user))
