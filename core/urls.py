from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
     path('dashboard/', views.dashboard, name='dashboard'),
     path('create-booking/', views.create_booking, name='create_booking'),
    path('', views.home, name='home'),
    path('add-room/', views.add_room, name='add_room'),
     path('view-rooms/', views.view_rooms, name='view_rooms'), 
     path('available-rooms-today/', views.available_rooms_today, name='available_rooms_today'),

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

    #path('dashboard/', views.dashboard, name='dashboard'),
    #path('create-booking/', views.create_booking, name='create_booking'),
    #path('rooms/', views.room_list, name='rooms'),
    #path('ajax/load-rooms/', views.load_rooms, name='ajax_load_rooms'),
    #path('approve/<int:booking_id>/', views.approve_booking, name='approve_booking'),
     #path('reject/<int:booking_id>/', views.reject_booking, name='reject_booking'),
     path('manage-bookings/', views.manage_bookings, name='manage_bookings'),
     path('booking/<int:booking_id>/', views.booking_detail, name='booking_detail'),
     path('approve/<int:booking_id>/', views.approve_booking, name='approve_booking'),
     path('reject/<int:booking_id>/', views.reject_booking, name='reject_booking'),
     path("approve-bookings/", views.approve_bookings, name="approve_bookings"),
]