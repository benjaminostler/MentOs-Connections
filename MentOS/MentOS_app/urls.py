from django.urls import path, re_path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='MentOS_app/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='MentOS_app/logout.html'), name='logout'),
    path('create-account/', views.create_account, name='create-account'),
    path('edit-profile/', views.edit_profile, name='edit-profile'),
    path('tips/', views.tips, name='tips'),
    path('delete-account/', views.delete_account, name='delete-account'),
    path('my-connections/', views.my_connections, name='my-connections'),
    re_path(r'^view-other-profiles/(?P<username_parameter>.*)/$', views.view_other_profiles, name='view-other-profiles'),
    path('chat/<str:room_name>/', views.room, name='room'),
    re_path(r'^send-email/(?P<username_parameter>.*)/$', views.send_email_to_user, name='send-email'),
    path('select-chat-room', views.select_chat_room, name='select-chat-room'),
]