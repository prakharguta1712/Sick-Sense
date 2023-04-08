from django.contrib import admin
from django.urls import path,include
from base import views
urlpatterns = [
    path('', views.home, name='home'),
    path('profile/<str:pk>/', views.userprofile, name='userprofile'),
    path('loginPage', views.loginPage, name='loginPage'),
    path('registerPage', views.registerPage, name='registerPage'),
    path('logoutPage', views.logoutPage, name='logoutPage'),
    path('room/<str:pk>/', views.room, name = 'room'),
    path('createRoom/', views.createRoom, name = 'createRoom'),
    path('updateRoom/<str:pk>/', views.updateRoom, name = 'updateRoom'),
    path('deleteRoom/<str:pk>/', views.deleteRoom, name = 'deleteRoom'),
    path('lung-cancer/', views.LungCancer, name = 'lung-cancer'),
    path('heart-attack/', views.HeartAttack, name = 'heart-attack'),
    path('kidney-disease/', views.KidneyDisease, name = 'kidney-disease'),
    path('daibetes/', views.Daibetes, name = 'daibetes'),

]
