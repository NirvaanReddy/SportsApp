
from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from . import user_endpoints
from . import search_endpoints
from . import workout_endpoints

def test_server(request):
    return HttpResponse("server is working")

urlpatterns = [
    path('login/', user_endpoints.user_login),
    path('',test_server),
    path('register/', user_endpoints.create_user),
    path('searchCategories/', search_endpoints.searchCategory),
    path('searchWorkouts/',search_endpoints.searchWorkouts),
    path('searchUsers/',search_endpoints.searchUsers),
    # path('getSavedWorkouts/', workout_endpoints.getSavedWorkouts),
    # path('getCompletedWorkouts/', workout_endpoints.getCompletedWorkouts),
    # path('getLikedWorkouts',workout_endpoints.getLikedWorkouts ),
    # path('saveWorkout/', workout_endpoints.saveWorkout),
    path('likeWorkout/', workout_endpoints.likeWorkout),
    path('unlikeWorkout/', workout_endpoints.unlikeWorkout),
    path('completeWorkout/', workout_endpoints.completeWorkout),
    path('publishWorkout/',workout_endpoints.publishWorkout),
    path('getWorkout/',workout_endpoints.getWorkout),
    path('downloadVideo/', workout_endpoints.downloadVideo),
    path('uploadVideo/',workout_endpoints.postVideo),
    path('getUserPreview/', user_endpoints.get_user_preview),
    path('update/', user_endpoints.update_user),
    path('follow/', user_endpoints.follow_user),
    path('unfollow/', user_endpoints.follow_user),
    path('getWorkout/', workout_endpoints.getWorkout),
    path('getWorkoutSession/', workout_endpoints.getWorkoutSession),
    path('resetPassword/', user_endpoints.reset_password),
    path('deleteWorkout/', user_endpoints.deleteWorkout),
    path('deleteWorkoutSession/', user_endpoints.deleteWorkoutSession),
    path('deleteUser/', user_endpoints.deleteUser)
    # path('publishWorkoutSession/', workout_endpoints.completeWorkout),
    #path('videos/')


    #path('pics',)
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