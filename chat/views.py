from django.shortcuts import render

def home(request):
    return render(request, 'index.html')

def room(request, room_name):
    return render(request, 'chatroom.html', {'room': room_name})
