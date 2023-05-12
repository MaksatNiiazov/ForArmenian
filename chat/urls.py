from django.urls import path

from . import views
from .views import SendMessage

urlpatterns = [
    path('<int:pk>/', views.room, name='chat_room'),
    path('send-message/<int:ad_id>', SendMessage.as_view(), name='send-message'),
]
