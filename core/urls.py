from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='desafios'),
    path('chat/', views.chat, name='chat'),
    path('chat/message/', views.chat_message, name='chat_message'),
    path('chat/new/', views.new_chat, name='new_chat'),
    path('historias/', views.historias, name='historias'),
    path('historias/read/', views.mark_story_read, name='mark_story_read'),
    path('trivias/', views.trivias, name='trivias'),
    path('trivias/<int:quiz_id>/', views.quiz_detail, name='quiz_detail'),
    path('trivias/submit/', views.submit_quiz, name='submit_quiz'),
    path('set-username/', views.set_username, name='set_username'),
]