from django.urls import path
from . import views
from .views import  *
 
urlpatterns = [
    path('',views.home,name='home'),
    
    path('teams/', views.team_list, name='team_list'),
    path('teams/new/', views.team_create, name='team_create'),
    path('teams/update/<int:pk>/', views.team_edit, name='team_edit'),
    path('teams/delete/<int:pk>/', TeamDeleteView.as_view(), name='team_delete'),

    path('drivers/', views.driver_list, name='driver_list'),
    path('drivers/new/', views.driver_create, name='driver_create'),
    path('drivers/edit/<int:pk>/', views.driver_edit, name='driver_edit'),
    path('drivers/delete/<int:pk>/', DriverDeleteView.as_view(), name='driver_delete'),

    path('races/', views.race_list, name='race_list'),
    path('races/new/', views.race_create, name='race_create'),  
    path('races/update/<int:pk>/', views.race_edit, name='race_edit'),
    path('races/delete/<int:pk>/', RaceDeleteView.as_view(), name='race_delete'),

    path('drivers/<int:driver_id>/race-register/', views.register_driver_to_race, name='register_driver_to_race'),
    path('races/<int:race_id>/edit-driver/', views.edit_race_drivers, name='edit_race_drivers'),

    
    
    
]