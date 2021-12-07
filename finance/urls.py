from django.urls import path
from finance.views import FinanceApi


urlpatterns = [
    path('finances/', FinanceApi.as_view()),
]
