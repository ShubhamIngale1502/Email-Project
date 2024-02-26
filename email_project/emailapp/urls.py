from django.urls import path
from .views import create_emp, details

urlpatterns = [
    path('add/', create_emp),
    path('add/<int:pk>/',details)
]
