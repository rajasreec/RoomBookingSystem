from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('add-room/', views.add_room, name='add_room'),
     path('view-rooms/', views.view_rooms, name='view_rooms'), 

    # Register (keep your custom register)
    path('register/', views.register_view, name='register'),

    # Built-in Login
    path('login/', 
         auth_views.LoginView.as_view(template_name='login.html'), 
         name='login'),

    # Built-in Logout
    path('logout/', 
         auth_views.LogoutView.as_view(), 
         name='logout'),

    path('dashboard/', views.dashboard, name='dashboard'),
    path('create-booking/', views.create_booking, name='create_booking'),
    path('rooms/', views.room_list, name='rooms'),
    path('ajax/load-rooms/', views.load_rooms, name='ajax_load_rooms'),
]