from django.urls import path
from . import views
urlpatterns = [
 path('', views.dashboard, name='dashboard'),
 path('players/', views.players, name='players'), path('players/add/', views.player_add, name='player_add'), path('players/<int:pk>/edit/', views.player_edit, name='player_edit'), path('players/<int:pk>/delete/', views.player_delete, name='player_delete'),
 path('teams/', views.teams, name='teams'), path('teams/add/', views.team_add, name='team_add'), path('teams/<int:pk>/delete/', views.team_delete, name='team_delete'),
 path('tournaments/', views.tournaments, name='tournaments'), path('tournaments/add/', views.tournament_add, name='tournament_add'), path('tournaments/<int:pk>/delete/', views.tournament_delete, name='tournament_delete'),
 path('compare/', views.compare, name='compare'), path('playing-xi/', views.playing_xi, name='playing_xi'),
]
