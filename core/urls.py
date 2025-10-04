from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='desafios'),
    path('chat/', views.chat, name='chat'),
    path('chat/message/', views.chat_message, name='chat_message'),
    path('chat/new/', views.new_chat, name='new_chat'),
    path('historias/', views.historias, name='historias'),
]