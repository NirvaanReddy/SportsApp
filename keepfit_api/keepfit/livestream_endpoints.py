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
    livestream = json.loads(request.body.decode("utf_8"))

    ls = Livestream.objects.create(id = livestream["id"], creatorID_id = livestream["creatorID"],
                                 url = livestream["url"], description = livestream["description"],
                                 date = livestream["date"])
    ls.save()
    return HttpResponse("true")

@api_view(['POST'])
def getLivestreams(request):
    livestreams = Livestream.objects.all()
    dicts = []
    for livestream in livestreams:
         dicts.append(livestream.toDict())
    response = json.dumps(dicts)

    return HttpResponse(response)

def deleteLivestream(request):
    return HttpResponse("to be implemented")