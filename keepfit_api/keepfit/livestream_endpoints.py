from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db import models
from .s import *
from .user import *
from django.core.files import File
from django.http import HttpResponse

import base64
import os
import json

@api_view(['POST'])
def publishLivestream(request):
    return HttpResponse("true")

@api_view(['POST'])
def getLivestreams(request):
    return HttpResponse("unbroken chain")