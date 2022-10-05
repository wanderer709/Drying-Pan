from django.urls import path
from .views import (
    TeamListView,
    UserTeamListView,
    TeamCreateView,
    TeamDetailView,
    TeamUpdateView,
    TeamDeleteView,
    PokemonListView,
    UserPokemonListView,
    PokemonCreateView,
    PokemonDetailView,
    PokemonUpdateView,
    PokemonDeleteView,
    TrainerView
)
from . import views

urlpatterns = [
    path('', views.home, name='pokemon-home'),
    path('trainers', views.trainers, name='pokemon-trainers'),
    path('trainer/<str:username>', TrainerView.as_view(), name='pokemon-trainer'),
    path('about', views.about, name='pokemon-about'),
    path('roster', PokemonListView.as_view(), name='pokemon-roster'),
    path('roster/<str:username>', UserPokemonListView.as_view(), name='user-pokemon-roster'),
    path('pokemon/new/', PokemonCreateView.as_view(), name='pokemon-create'),
    path('pokemon/<int:pk>/', PokemonDetailView.as_view(), name='pokemon-detail'),
    path('pokemon/<int:pk>/update', PokemonUpdateView.as_view(), name='pokemon-update'),
    path('pokemon/<int:pk>/delete', PokemonDeleteView.as_view(), name='pokemon-delete'),
    path('teams', TeamListView.as_view(), name='pokemon-teams'),
    path('teams/<str:username>', UserTeamListView.as_view(), name='user-pokemon-teams'),
    path('team/new/', TeamCreateView.as_view(), name='team-create'),
    path('team/<int:pk>/', TeamDetailView.as_view(), name='team-detail'),
    path('team/<int:pk>/update', TeamUpdateView.as_view(), name='team-update'),
    path('team/<int:pk>/delete', TeamDeleteView.as_view(), name='team-delete'),
    # path('pokemon', views.pokemon, name='pokemon-pokemon'),
    # path('team', views.team, name='pokemon-team'),
]
