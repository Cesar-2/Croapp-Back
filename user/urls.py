from django.urls import path, include
from user.views import UserApi, UserLoginApi, UserEarnApi


urlpatterns = [
    path('register', UserApi.as_view()),
    path('login', UserLoginApi.as_view()),
    path('', UserEarnApi.as_view()),
]
