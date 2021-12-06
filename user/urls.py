from django.urls import path, include
from user.views import UserApi


urlpatterns = [
    path('register/', UserApi.as_view()),
]
