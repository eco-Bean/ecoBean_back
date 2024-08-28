# main/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('main/<int:user_id>/', views.main_page, name='main_page'),
    path('accomplish-mission/', views.accomplish_mission, name='accomplish_mission'),
]
