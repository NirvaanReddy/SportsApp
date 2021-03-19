from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db import models
from .s import *
from .models import User
from django.core.files import File

import base64
import os
import json

# + func getWorkoutCategories(w http.ResponseWriter, r *http.Request)
# + func getSavedWorkouts(w http.ResponseWriter, r *http.Request)
# + func getCompletedWorkouts(w http.ResponseWriter, r *http.Request)
# + func saveWorkout(w http.ResponseWriter, r *http.Request)
# + func publishWorkout(w http.ResponseWriter, r *http.Request)
# + func downloadWorkoutVideos(w http.ResponseWriter, r *http.Request)
# + func completedWorkout(w http.ResponseWriter, r *http.Request)

@api_view(['POST'])
def get_workout_categories(request):
    pass

@api_view(['POST'])
def getSavedWorkouts( rWriter,httpReq):
    pass





