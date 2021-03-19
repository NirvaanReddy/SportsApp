
from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from . import views


urlpatterns = [
    path('login/', views.user_login),
    path('register/', views.user_registration)
]