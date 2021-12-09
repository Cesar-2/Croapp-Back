from django.urls import path
from landingpage.views import LandingPageApi

urlpatterns = [
    path('content', LandingPageApi.as_view())
]
