from django.urls import path
from .views import chat, chat_history

urlpatterns = [
    path('question', chat, name='create_question'),
    path('history', chat_history, name='chat_history'),
]