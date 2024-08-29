from django.urls import path
from .views import get_location

urlpatterns = [
    path('location', get_location, name='location'),
]