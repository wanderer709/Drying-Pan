from django.shortcuts import render, get_object_or_404
from django.views.generic import (
    ListView, 
    CreateView,
    DetailView, 
    UpdateView,
    DeleteView
)
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Team, Pokemon
from .forms import (
    TeamCreateForm,
    TeamUpdateForm,
    PokemonCreateForm,
    PokemonUpdateForm,
)
from .pokedict import pokedict
import os
from PIL import Image
import requests
# import pokebase as pb

context = 54

# Create your views here.
def home(request):
    module_dir = os.path.dirname(__file__)
    file_path = os.path.join(module_dir, 'pokemon_breeds.dat')
    file = open(file_path, 'r', encoding='utf-8')
    breeds_list = file.readlines()
    # # karp = pb.pokemon(128).sprites.front_default
    karp = requests.get(f'https://pokeapi.co/api/v2/pokemon/{pokedict["Magikarp"]}')
    karp = karp.json()['sprites']['front_default']
    # img = Image.open(karp)
    context = {
        'breeds': breeds_list,
        'karp': karp
    }
    return render(request, 'pokemon/home.html', {'context': context})


def about(request):
    return render(request, 'pokemon/about.html', {'title': 'About'})

def trainers(request):
    # context = {
    #     'users': User.objects.all(),
    #     'title': 'Trainers'
    # }
    return render(request, 'pokemon/trainers.html', {'users': User.objects.all(), 'title': 'Trainers'})


class TrainerView(ListView):
    model = User
    template_name = 'pokemon/trainer.html' 
    context_object_name = 'trainer'

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return User.objects.filter(username=user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = User.objects.filter(username=self.kwargs.get('username')).first()
        context['title'] = f'{self.kwargs.get("username")}'
        return context


class PokemonListView(ListView):
    model = Pokemon
    template_name = 'pokemon/roster.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'pokemon'
    paginate_by = 12
    ordering = ['-date_created']

    def get_queryset(self):
        # user = get_object_or_404(User, user=self.request.user)
        return Pokemon.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        module_dir = os.path.dirname(__file__)
        types_file_path = os.path.join(module_dir, 'pokemon_types.dat')
        with open(types_file_path, 'r', encoding='utf-8') as f:
            types_list = f.readlines()
        types_pics_list = []
        for types in types_list:
            types_pics_list.append(types[:-1].lower())

        context = super().get_context_data(**kwargs)
        context['types_pics_list'] = types_pics_list
        context['title'] = 'Roster'
        return context

class UserPokemonListView(ListView):
    model = Pokemon
    template_name = 'pokemon/user_roster.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'pokemon'
    paginate_by = 12
    ordering = ['-date_created']

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Pokemon.objects.filter(user=user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Roster - {self.kwargs.get("username")}'
        return context


class PokemonDetailView(DetailView):
    model = Pokemon

    def get_context_data(self, **kwargs):
        module_dir = os.path.dirname(__file__)
        types_file_path = os.path.join(module_dir, 'pokemon_types.dat')
        with open(types_file_path, 'r', encoding='utf-8') as f:
            types_list = f.readlines()
        types_pics_list = []
        for types in types_list:
            types_pics_list.append(types[:-1].lower())

        context = super().get_context_data(**kwargs)
        context['types_pics_list'] = types_pics_list
        # context['title'] = self.kwargs.get("name")
        return context



class PokemonCreateView(LoginRequiredMixin, CreateView):
    model = Pokemon
    form_class = PokemonCreateForm


    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        module_dir = os.path.dirname(__file__)
        types_file_path = os.path.join(module_dir, 'pokemon_types.dat')
        moves_file_path = os.path.join(module_dir, 'pokemon_moves.dat')
        abilities_file_path = os.path.join(module_dir, 'pokemon_abilities.dat')
        items_file_path = os.path.join(module_dir, 'pokemon_items.dat')
        natures_file_path = os.path.join(module_dir, 'pokemon_natures.dat')
        characteristics_file_path = os.path.join(module_dir, 'pokemon_characteristics.dat')
        breeds_list = []
        for breed in pokedict.keys():
            breeds_list.append(breed)
        with open(moves_file_path, 'r', encoding='utf-8') as f:
            moves_list = f.readlines()
        with open(types_file_path, 'r', encoding='utf-8') as f:
            types_list = f.readlines()
        with open(abilities_file_path, 'r', encoding='utf-8') as f:
            abilities_list = f.readlines()
        with open(items_file_path, 'r', encoding='utf-8') as f:
            items_list = f.readlines()
        with open(natures_file_path, 'r', encoding='utf-8') as f:
            natures_list = f.readlines()
        with open(characteristics_file_path, 'r', encoding='utf-8') as f:
            characteristics_list = f.readlines()
        context = super().get_context_data(**kwargs)
        context['breeds_list'] = breeds_list
        context['types_list'] = types_list
        context['moves_list'] = moves_list
        context['abilities_list'] = abilities_list
        context['items_list'] = items_list
        context['natures_list'] = natures_list
        context['characteristics_list'] = characteristics_list

        return context

class PokemonUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Pokemon
    form_class = PokemonUpdateForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        module_dir = os.path.dirname(__file__)
        breeds_file_path = os.path.join(module_dir, 'pokemon_breeds.dat')
        types_file_path = os.path.join(module_dir, 'pokemon_types.dat')
        moves_file_path = os.path.join(module_dir, 'pokemon_moves.dat')
        abilities_file_path = os.path.join(module_dir, 'pokemon_abilities.dat')
        items_file_path = os.path.join(module_dir, 'pokemon_items.dat')
        natures_file_path = os.path.join(module_dir, 'pokemon_natures.dat')
        characteristics_file_path = os.path.join(module_dir, 'pokemon_characteristics.dat')
        with open(breeds_file_path, 'r', encoding='utf-8') as f:
            breeds_list = f.readlines()
        with open(moves_file_path, 'r', encoding='utf-8') as f:
            moves_list = f.readlines()
        with open(types_file_path, 'r', encoding='utf-8') as f:
            types_list = f.readlines()
        with open(abilities_file_path, 'r', encoding='utf-8') as f:
            abilities_list = f.readlines()
        with open(items_file_path, 'r', encoding='utf-8') as f:
            items_list = f.readlines()
        with open(natures_file_path, 'r', encoding='utf-8') as f:
            natures_list = f.readlines()
        with open(characteristics_file_path, 'r', encoding='utf-8') as f:
            characteristics_list = f.readlines()
        context = super().get_context_data(**kwargs)
        context['breeds_list'] = breeds_list
        context['types_list'] = types_list
        context['moves_list'] = moves_list
        context['abilities_list'] = abilities_list
        context['items_list'] = items_list
        context['natures_list'] = natures_list
        context['characteristics_list'] = characteristics_list

        return context

    def test_func(self):
        obj = self.get_object()
        if self.request.user == obj.user:
            return True
        return False


class PokemonDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Pokemon
    success_url = '/roster'

    def test_func(self):
        obj = self.get_object()
        if self.request.user == obj.user:
            return True
        return False
        

class TeamListView(ListView):
    model = Team
    template_name = 'pokemon/teams.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'teams'
    paginate_by = 6
    ordering = ['-date_created']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Teams'
        return context


class UserTeamListView(ListView):
    model = Team
    template_name = 'pokemon/user_teams.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'teams'
    paginate_by = 6
    ordering = ['-date_created']

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Team.objects.filter(user=user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Teams - {self.kwargs.get("username")}'
        return context


class TeamDetailView(DetailView):
    model = Team

    # def get_queryset(self):
    #     # user = get_object_or_404(User, user=self.request.user)
    #     return Pokemon.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        module_dir = os.path.dirname(__file__)
        types_file_path = os.path.join(module_dir, 'pokemon_types.dat')
        with open(types_file_path, 'r', encoding='utf-8') as f:
            types_list = f.readlines()
        types_pics_list = []
        for types in types_list:
            types_pics_list.append(types[:-1].lower())

        context = super().get_context_data(**kwargs)
        context['types_pics_list'] = types_pics_list
        context['title'] = context['team']
        return context


class TeamCreateView(LoginRequiredMixin, CreateView):
    model = Team
    form_class = TeamCreateForm

    def get_form_kwargs(self):
        kwargs = super(TeamCreateView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        for pokemon in form.instance.main.all():
            pokemon.team = form.instance
            pokemon.save()
        for pokemon in form.instance.box.all():
            pokemon.team = form.instance
            pokemon.save()
        teams = Team.objects.filter(user = self.request.user)
        poke_pool = Pokemon.objects.filter(user = self.request.user)
        for pokemon in poke_pool:
            in_team = False
            for team in teams:
                if pokemon in team.main.all() or pokemon in team.box.all():
                    in_team = True
            if not in_team:
                pokemon.team = None
                pokemon.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        module_dir = os.path.dirname(__file__)
        games_file_path = os.path.join(module_dir, 'pokemon_games.dat')
        regions_file_path = os.path.join(module_dir, 'pokemon_regions.dat')
        with open(games_file_path, 'r', encoding='utf-8') as f:
            games_list = f.readlines()
        with open(regions_file_path, 'r', encoding='utf-8') as f:
            regions_list = f.readlines()
        context = super().get_context_data(**kwargs)
        context['games_list'] = games_list
        context['regions_list'] = regions_list

        return context


class TeamUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Team
    form_class = TeamUpdateForm

    def get_form_kwargs(self):
        kwargs = super(TeamUpdateView, self).get_form_kwargs(
        )
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        for pokemon in form.instance.main.all():
            pokemon.team = form.instance
            pokemon.save()
        for pokemon in form.instance.box.all():
            pokemon.team = form.instance
            pokemon.save()
        teams = Team.objects.filter(user = self.request.user)
        poke_pool = Pokemon.objects.filter(user = self.request.user)
        for pokemon in poke_pool:
            in_team = False
            for team in teams:
                if pokemon in team.main.all() or pokemon in team.box.all():
                    in_team = True
            if not in_team:
                pokemon.team = None
                pokemon.save()        
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        module_dir = os.path.dirname(__file__)
        games_file_path = os.path.join(module_dir, 'pokemon_games.dat')
        regions_file_path = os.path.join(module_dir, 'pokemon_regions.dat')
        with open(games_file_path, 'r', encoding='utf-8') as f:
            games_list = f.readlines()
        with open(regions_file_path, 'r', encoding='utf-8') as f:
            regions_list = f.readlines()
        context = super().get_context_data(**kwargs)
        context['games_list'] = games_list
        context['regions_list'] = regions_list

        return context

    def test_func(self):
        obj = self.get_object()
        if self.request.user == obj.user:
            return True
        return False


class TeamDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Team
    success_url = '/teams'

    def test_func(self):
        obj = self.get_object()
        if self.request.user == obj.user:
            return True
        return False
