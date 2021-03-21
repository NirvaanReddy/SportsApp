
from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from . import user_endpoints
from . import search_endpoints
from . import workout_endpoints


urlpatterns = [
    path('login/', user_endpoints.user_login),
    path('register/', user_endpoints.user_registration),
    path('searchCaterogies/', search_endpoints.searchCategories),
    path('searchWorkouts/',search_endpoints.searchWorkouts),
    path('searchUsers/',search_endpoints.searchUsers),
    path('getSavedWorkouts/', workout_endpoints.getSavedWorkouts),
    path('getCompletedWorkouts/', workout_endpoints.getCompletedWorkouts),
    path('saveWorkout/', workout_endpoints.saveWorkout),
    path('publishWorkout/',workout_endpoints.publishWorkout),
    path('getWorkout/',workout_endpoints.getWorkout),
    path('completedWorkout/',workout_endpoints.completedWorkout),
    path('downloadVideo/', workout_endpoints.downloadVideo),
    path('videos/')
]
# getUserPreview(id: String) -> UserPreview
# PATH = "getUser" // do this for each endpoint so on the front end I know where to send each of the HTTP Requests
# registerUser(user: User) -> Bool
# updateUser(user: User)
# attemptLogin(username: String, password: String) -> LoginResult
# followUser(otherID: String)
#
# getWorkout(id: String) -> Workout
# publishWorkout(workout: Workout)
# getWorkoutSession(id: String) -> WorkoutSession
# publishWorkoutSession(session: WorkoutSession)
# downloadVideoToURL(workoutID: String) -> RAWDATA
# publishVideo(data: RAWDATA) // there will be a parameter in the URL that has the id of the user
# // use this id to save the raw data to the file system
#
# get10Users(prefix: String) -> [UserPreview]
# get10Workouts(prefix: String) -> [Workout]