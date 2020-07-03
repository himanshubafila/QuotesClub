from django.contrib import admin

# Register your models here.
from .models import Contact ,  Post , Profile , Comment , Follower , Following ,Like , MyLike , SavePost , MySave , HashTag , Blocking , MyBlocking , Notifications , MyNotifacions

admin.site.register((Contact ,  Post , Profile , Comment , Follower , Following , Like , MyLike ,  SavePost , MySave , HashTag, Blocking , MyBlocking , Notifications , MyNotifacions ))