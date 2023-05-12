from urllib import request

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views import View

from forarmenians_app.models import Ad
from chat.models import Room, Message, UsersInRoom


@login_required
def room(request, pk):
    room = Room.objects.get(id=pk)
    messages = Message.objects.filter(room=room)

    return render(request, 'chat/room.html', {'room': room, 'messages': messages})


class SendMessage(View):
    def post(self, request, ad_id):
        ad = Ad.objects.get(id=ad_id)
        room_new = Room.objects.get_or_create(ad=ad, name=ad.title, sender_id=self.request.user.id)
        room = Room.objects.get(ad=ad, name=ad.title, sender=self.request.user.id)
        send_message = Message.objects.create(room_id=room.id, user_id=self.request.user.id, content=self.request.POST.get('message'))
        connect_first_user = UsersInRoom.objects.get_or_create(room_id=room.id, user_id=self.request.user.id)
        connect_second_user = UsersInRoom.objects.get_or_create(room_id=room.id, user_id=ad.created_by.id)
        return redirect('chat_room', room.id)

