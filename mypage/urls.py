# mypage/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('mypage/', views.user_profile_detail, name='user_profile_detail'),
    path('mypage/upload-challenge/', views.upload_challenge_image, name='upload_challenge_image'),
]
