from django.urls import path
from . import views

urlpatterns = [
    path('', views.room_list, name='room_list'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('room/<str:room_name>/', views.room, name='room'),
    path('dm/<str:username>/', views.direct_chat, name='direct_chat'),
    path('register/', views.register, name='register'),
]