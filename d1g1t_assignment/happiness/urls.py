from django.urls import path

from . import views

urlpatterns = [
    path('submit/', views.happinessSubmit, name='submit'),
    path('stat/', views.happinessStatistics, name='stat'),
    path('team/', views.teamView, name='team'),
    path('member/',views.memberView, name='member')
]