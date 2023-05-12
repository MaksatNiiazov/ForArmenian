from django.db import models
from forarmenians_app.models import Ad
from user_auth.models import User


class Room(models.Model):
    name = models.CharField(max_length=255)
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='rooms')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rooms')


class UsersInRoom(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chats')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='chats')


class Message(models.Model):
    room = models.ForeignKey(Room, related_name='messages', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-date_added',)
