from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('register', views.register, name='register'),
    path('user_home', views.user_home, name='user_home'),
    path('profile/<str:username>', views.profile, name='profile'),
    path('edit_profile/<str:username>', views.edit_profile, name='edit_profile'),
    path('reset_password/<str:username>', views.reset_password, name='reset_password'),
    path('super', views.super, name='super'),
    path('manage_user', views.manage_user, name='manage_user'),
    path('forgot', views.forgot, name='forgot'),
    path('admin_alluser', views.admin_alluser, name='admin_alluser'),
    path('admin_editprofile/<str:username>', views.admin_editprofile, name='admin_editprofile'),
    path('change_role', views.change_role, name='change_role'),
    path('admin_passreset', views.admin_passreset, name='admin_passreset'),
    path('add_user', views.add_user, name='add_user'),
    path('delete_user', views.delete_user, name='delete_user'),
    path('test', views.test, name='test')
    
]
