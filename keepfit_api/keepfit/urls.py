
from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from . import user_endpoints


urlpatterns = [
    path('login/', user_endpoints.user_login),
    path('register/', user_endpoints.user_registration)
]