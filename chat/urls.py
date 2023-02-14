from django.urls import path
from .views import home, room

urlpatterns = [
    path("", home, name = "Home"),
    path("<str:room_name>/", room, name = "Room"),
    
]
