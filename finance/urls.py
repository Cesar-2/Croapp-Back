from django.urls import path
from finance.views import FinanceApi, CostApi


urlpatterns = [
    path('finances', FinanceApi.as_view()),
    path('cost', CostApi.as_view()),
]
