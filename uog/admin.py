from django.contrib import admin
from .models import Profile, Post, LikePost, FollowersCount, ChatMessage, Files

# Register your models here.
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(LikePost)
admin.site.register(FollowersCount)
admin.site.register(ChatMessage)
admin.site.register(Files)