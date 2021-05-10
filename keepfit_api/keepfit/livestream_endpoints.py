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
def attemptToEnterLivestream(request):

    tup = json.loads(request.body.decode("utf_8"))

    userID = tup["userID"]
    livestreamID = tup["livestreamID"]

    livestream = Livestream.objects.get(id=livestreamID)

    if livestream.getNumberOfParticipants() < livestream.maximumParticipants:
        lp = LivestreamParticipant.objects.create(user_id=userID,livestream_id=livestreamID)
        lp.save()
        return HttpResponse("true")
    else:
        return HttpResponse("false")


@api_view(['POST'])
def leaveLivestream(request):

    tup = json.loads(request.body.decode("utf_8"))

    userID = tup["userID"]
    livestreamID = tup["livestreamID"]

    LivestreamParticipant.objects.filter(livestream_id=livestreamID).filter(user_id=userID).delete()
    return HttpResponse("true")

@api_view(['POST'])
def publishLivestream(request):
    livestream = json.loads(request.body.decode("utf_8"))

    ls = Livestream.objects.create(id = livestream["id"], creatorID_id = livestream["creatorID"],
                                 url = livestream["url"], description = livestream["description"],
                                 date = livestream["date"], maximumParticipants = livestream["maximumParticipants"])
    ls.save()
    return HttpResponse("true")

@api_view(['POST'])
def getLivestreams(request):
    userID = json.loads(request.body.decode("utf_8"))
    livestreams = Livestream.objects.all()
    dicts = []
    for livestream in livestreams:
        livestreamDict = livestream.toDict(userID=userID)
        dicts.append(livestreamDict)

    response = json.dumps(dicts)

    return HttpResponse(response)

def deleteLivestream(request):
    id = json.loads(request.body.decode("utf_8"))

    Livestream.objects.filter(id=id).delete()
    return HttpResponse("true")