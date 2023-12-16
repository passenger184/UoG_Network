from  django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('discover', views.home, name='home'),
    path('signup', views.signup, name='signup'),
    path('signin', views.signin, name='signin'),
    path('logout', views.logout, name='logout'),
    path('settings', views.settings, name='settings'),
    path('upload', views.upload, name='upload'),
    path('like-post', views.like_post, name='like-post'),
    path('profile/<str:pk>', views.profile, name='profile'),
    path('follow', views.follow, name='follow'),
    path('search', views.search, name='search'),
    path('files', views.files, name='files'),
    path('files/open<str:id>', views.show, name='show'),
    path('chat', views.chat, name='chat'),
    path('uog_chat/<str:pk>', views.uog_chat, name="uog_chat"),
    path('sent_msg/<str:pk>', views.sentMessages, name = "sent_msg"),
    path('rec_msg/<str:pk>', views.receivedMessages, name = "rec_msg"),
    path('notification', views.chatNotification, name = "notification"),
]












