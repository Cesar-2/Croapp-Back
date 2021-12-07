from django.urls import path, include
from user.views import UserApi, UserLoginApi


urlpatterns = [
    path('register/', UserApi.as_view()),
    path('login/', UserLoginApi.as_view()),
]
