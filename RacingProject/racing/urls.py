from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import  *

router = DefaultRouter()
router.register(r'teams', TeamViewSet)
router.register(r'drivers', DriverViewSet)
router.register(r'races', RaceViewSet)

urlpatterns = [
    path('home/',views.home,name='home'),

    path('team/', views.team_list, name='team_list'),
    path('team/new/', views.team_create, name='team_create'),
    path('team/update/<int:pk>/', views.team_edit, name='team_edit'),
    path('team/delete/<int:pk>/', TeamDeleteView.as_view(), name='team_delete'),

    path('driver/', views.driver_list, name='driver_list'),
    path('driver/new/', views.driver_create, name='driver_create'),
    path('driver/edit/<int:pk>/', views.driver_edit, name='driver_edit'),
    path('driver/delete/<int:pk>/', DriverDeleteView.as_view(), name='driver_delete'),

    path('race/', views.race_list, name='race_list'),
    path('race/new/', views.race_create, name='race_create'),  
    path('race/update/<int:pk>/', views.race_edit, name='race_edit'),
    path('race/delete/<int:pk>/', RaceDeleteView.as_view(), name='race_delete'),

    path('driver/<int:driver_id>/race-register/', views.register_driver_to_race, name='register_driver_to_race'),
    path('race/<int:race_id>/edit-driver/', views.edit_race_drivers, name='edit_race_drivers'),

#API views urls
    path('', include(router.urls)),
   
    path('races/<int:race_id>/add-drivers/', AddDriversToRaceAPIView.as_view(), name='add-drivers-to-race'),
    path('drivers/<int:driver_id>/add-races/', AddRacesToDriverAPIView.as_view(), name='add-races-to-driver'),

    
    
    
]