from django.urls import path
from .views import chat, chat_history, recycle

urlpatterns = [
    path('question', chat, name='create_question'),
    path('history', chat_history, name='chat_history'),
    path('recycle', recycle, name='recycle'),
]