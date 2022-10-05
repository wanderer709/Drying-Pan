from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.urls import reverse
from .pokedict import pokedict
import requests
import os


class Pokemon(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    name = models.CharField(max_length=15)
    breed = models.CharField(max_length=25, default='N')
    type1 = models.CharField(max_length=15, null=True, blank=True)
    type2 = models.CharField(max_length=15, null=True, blank=True)
    form = models.CharField(max_length=15, null=True, blank=True)
    is_shiny = models.BooleanField(default=False)
    GENDERS = [
        ('♂', 'Male'),
        ('♀', 'Female'),
        (' ', 'Genderless')
    ]
    gender = models.CharField(
        choices=GENDERS, max_length=1, default=' ', null=True, blank=True)
    ability = models.CharField(max_length=15, null=True, blank=True)
    nature = models.CharField(max_length=15, null=True, blank=True)
    item = models.CharField(max_length=15, null=True, blank=True)
    move1 = models.CharField(max_length=20, null=True, blank=True)
    move2 = models.CharField(max_length=20, null=True, blank=True)
    move3 = models.CharField(max_length=20, null=True, blank=True)
    move4 = models.CharField(max_length=20, null=True, blank=True)
    level = models.PositiveIntegerField(validators=[MinValueValidator(
        1), MaxValueValidator(100)], null=True, blank=True)
    hp = models.PositiveIntegerField(
        validators=[MinValueValidator(1)], null=True, blank=True)
    attack = models.PositiveIntegerField(
        validators=[MinValueValidator(1)], null=True, blank=True)
    defense = models.PositiveIntegerField(
        validators=[MinValueValidator(1)], null=True, blank=True)
    spec_atk = models.PositiveIntegerField(
        validators=[MinValueValidator(1)], null=True, blank=True)
    spec_def = models.PositiveIntegerField(
        validators=[MinValueValidator(1)], null=True, blank=True)
    speed = models.PositiveIntegerField(
        validators=[MinValueValidator(1)], null=True, blank=True)
    charactaristic = models.TextField(null=True, blank=True)
    met = models.TextField(null=True, blank=True)
    team = models.ForeignKey(
        'Team', on_delete=models.CASCADE, default=None, null=True, blank=True)
    remarks = models.TextField(null=True, blank=True)
    date_created = models.DateTimeField(default=timezone.now)

    @property
    def sprite(self):
        try:
            pokedex_num = pokedict[self.breed]
            response = requests.get(f'https://pokeapi.co/api/v2/pokemon/{pokedex_num}')
            if self.gender == 'F' and response.json()['sprites']['front_female']:
                return response.json()['sprites']['front_female']
            return response.json()['sprites']['front_default']
        except:
            return '/media/pokemon/default.jpg'

    @property
    def type_1(self):
        if not self.type1:
            try:
                pokedex_num = pokedict[self.breed]
                response = requests.get(f'https://pokeapi.co/api/v2/pokemon/{pokedex_num}')
                return response.json()['types'][0]['type']['name']
            except:
                return ''

    @property
    def type_2(self):
        if not self.type2:
            try:
                pokedex_num = pokedict[self.breed]
                response = requests.get(f'https://pokeapi.co/api/v2/pokemon/{pokedex_num}')
                return response.json()['types'][1]['type']['name']
            except:
                return ''

    class Meta:
        ordering = ['-date_created']

    # @type1.setter
    # def type1(self, value):
        

    def __str__(self):
        return f'{self.name} ({self.breed})'

    def get_absolute_url(self):
        return reverse('pokemon-detail', kwargs={'pk': self.pk})


class Team(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    name = models.CharField(max_length=15)
    teamname = models.CharField(max_length=15)
    game = models.CharField(max_length=15)
    victories = models.PositiveIntegerField(default=0)
    formal_defeats = models.PositiveIntegerField(default=0)
    total_defeats = models.PositiveIntegerField(default=0)
    REGIONS = 'automatically match each region to each existing game and allow for custom'
    region = models.CharField(max_length=15)
    id_no = models.PositiveIntegerField(
        validators=[MaxValueValidator(999999)], null=True, blank=True)
    pokedex_seen = models.PositiveIntegerField(
        validators=[MaxValueValidator(901)], null=True, blank=True)
    pokedex_caught = models.PositiveIntegerField(
        validators=[MaxValueValidator(901)], null=True, blank=True)
    money = models.PositiveIntegerField(null=True, blank=True)
    date_started = models.DateField(null=True, blank=True)
    time_hours = models.PositiveIntegerField(default=0, null=True, blank=True)
    time_minutes = models.PositiveIntegerField(default=0, 
                                               validators=[MaxValueValidator(59)], null=True, blank=True)
    badges = models.PositiveIntegerField(default=0,
                                         validators=[MaxValueValidator(16)], null=True, blank=True)
    hall_of_fame = models.DateField(null=True, blank=True)
    main = models.ManyToManyField(
        Pokemon, default=None, related_name='+', blank=True)
    box = models.ManyToManyField(
        Pokemon, related_name='+', default=None, blank=True)
    remarks = models.TextField(null=True, blank=True)
    title = 'Teams'
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.teamname

    def get_absolute_url(self):
        return reverse('team-detail', kwargs={'pk': self.pk})

    # limit_choices_to = {'user': user.primary_key}
    def limit_main(self):
        return {'user': self.user}

    class Meta:
        ordering = ['-date_created']
