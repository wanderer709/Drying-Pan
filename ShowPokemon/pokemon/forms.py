from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from .models import Team, Pokemon

class CustomMMCF(forms.ModelMultipleChoiceField):

    def label_from_instance(self, pokemon):
        return '%s' % pokemon.name

class TeamCreateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(TeamCreateForm, self).__init__(*args, **kwargs)
        self.fields['main'].queryset = Pokemon.objects.filter(user=self.request.user).filter(team=None)
        self.fields['box'].queryset = Pokemon.objects.filter(user=self.request.user).filter(team=None)

    class Meta:
        model = Team
        fields = [
            'name',
            'teamname',
            'victories',
            'formal_defeats',
            'total_defeats',
            'game',
            'region',
            'id_no',
            'pokedex_seen',
            'pokedex_caught',
            'money',
            'date_started',
            'time_hours',
            'time_minutes',
            'badges',
            'hall_of_fame',
            'main',
            'box',
            'remarks'
        ]
        widgets = {
            'time_hours': forms.NumberInput(attrs={'style': 'width:3rem;'}),
            'time_minutes': forms.NumberInput(attrs={'style': 'width:3rem;'}),
            'game': forms.TextInput(attrs={'list': 'pokemon-games', 'name': 'pokemon-games', 'autocomplete': 'on'}),
            'region': forms.TextInput(attrs={'list': 'pokemon-regions', 'name': 'pokemon-region', 'autocomplete': 'on'}),
        }
        error_messages = {
            'time_minutes': {
                'max_value': _('There is only 60 minute in an hour, silly. Make sure the minute value is 59 or lower.')
            }
        }

    def clean(self):
        cleaned_data = super().clean()
        main = cleaned_data.get('main')
        box = cleaned_data.get('box')
        if main and main.count() > 6:
            self.add_error('main', ValidationError('Maximum of six Pokémon allowed for your main team.'))
        if bool(set(main) & set(box)):
            self.add_error('box', ValidationError('None of your Pokémon can be in both your main team and your box'))


    main = forms.ModelMultipleChoiceField(
        queryset=None,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    box = forms.ModelMultipleChoiceField(
        queryset=None,
        widget=forms.CheckboxSelectMultiple,
        required=False, 
    )


class TeamUpdateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(TeamUpdateForm, self).__init__(*args, **kwargs)
        path = self.request.path_info
        current_team_id = int(path[path.find('/team')+6:path.find('/update')])
        poke_pool = Pokemon.objects.filter(user=self.request.user).filter(Q(team=current_team_id) | Q(team=None))
        self.fields['main'].queryset = poke_pool
        self.fields['box'].queryset = poke_pool

    class Meta:
        model = Team
        fields = [
            'name',
            'teamname',
            'victories',
            'formal_defeats',
            'total_defeats',
            'game',
            'region',
            'id_no',
            'pokedex_seen',
            'pokedex_caught',
            'money',
            'date_started',
            'time_hours',
            'time_minutes',
            'badges',
            'hall_of_fame',
            'main',
            'box',
            'remarks'
        ]
        widgets = {
            'time_hours': forms.NumberInput(attrs={'style': 'width:3rem;'}),
            'time_minutes': forms.NumberInput(attrs={'style': 'width:3rem;'}),
            'game': forms.TextInput(attrs={'list': 'pokemon-games', 'name': 'pokemon-games', 'autocomplete': 'on'}),
            'region': forms.TextInput(attrs={'list': 'pokemon-regions', 'name': 'pokemon-region', 'autocomplete': 'on'}),
        }
        error_messages = {
            'time_minutes': {
                'max_value': _('There is only 60 minute in an hour, silly. Make sure the minute value is 59 or lower.')
                }
            }


    def clean(self):
        cleaned_data = super().clean()
        main = cleaned_data.get('main')
        box = cleaned_data.get('box')
        if main and main.count() > 6:
            self.add_error('main', 'Maximum of six Pokémon allowed for your main team.')
        if bool(set(main) & set(box)):
            self.add_error('box', 'None of your Pokémon can be in both your main team and your box')
        
    main = forms.ModelMultipleChoiceField(
        queryset=None,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    box = forms.ModelMultipleChoiceField(
        queryset=None,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )


class PokemonCreateForm(forms.ModelForm):
    class Meta:
        model = Pokemon
        fields = [
            'name',
            'breed',
            'type1',
            'type2',
            'gender',
            'ability',
            'nature',
            'item',
            'move1',
            'move2',
            'move3',
            'move4',
            'level',
            'hp',
            'attack',
            'defense',
            'spec_atk',
            'spec_def',
            'speed',
            'charactaristic',
            'met',
            'remarks'
        ]
        widgets = {
            'breed': forms.TextInput(attrs={'list': 'pokemon-breeds', 'name':'pokemon-breeds', 'autocomplete': 'on'}),
            'type1': forms.TextInput(attrs={'list': 'pokemon-types', 'name': 'pokemon-type1', 'autocomplete': 'on'}),
            'type2': forms.TextInput(attrs={'list': 'pokemon-types', 'name': 'pokemon-type2', 'autocomplete': 'on'}),
            'move1': forms.TextInput(attrs={'list': 'pokemon-moves', 'name': 'pokemon-move1', 'autocomplete': 'on'}),
            'move2': forms.TextInput(attrs={'list': 'pokemon-moves', 'name': 'pokemon-move2', 'autocomplete': 'on'}),
            'move3': forms.TextInput(attrs={'list': 'pokemon-moves', 'name': 'pokemon-move3', 'autocomplete': 'on'}),
            'move4': forms.TextInput(attrs={'list': 'pokemon-moves', 'name': 'pokemon-move4', 'autocomplete': 'on'}),
            'ability': forms.TextInput(attrs={'list': 'pokemon-abilities', 'name': 'pokemon-abilities', 'autocomplete': 'on'}),
            'nature': forms.TextInput(attrs={'list': 'pokemon-natures', 'name': 'pokemon-natures', 'autocomplete': 'on'}),
            'item': forms.TextInput(attrs={'list': 'pokemon-items', 'name': 'pokemon-items', 'autocomplete': 'on'}),
            'characteristic': forms.TextInput(attrs={'list': 'pokemon-characteristics', 'name': 'pokemon-characteristic', 'autocomplete': 'on'}),
        }


class PokemonUpdateForm(forms.ModelForm):
    class Meta:
        model = Pokemon
        fields = [
            'name',
            'breed',
            'type1',
            'type2',
            'gender',
            'ability',
            'nature',
            'item',
            'move1',
            'move2',
            'move3',
            'move4',
            'level',
            'hp',
            'attack',
            'defense',
            'spec_atk',
            'spec_def',
            'speed',
            'charactaristic',
            'met',
            'remarks'
        ]
        widgets = {
            'breed': forms.TextInput(attrs={'list': 'pokemon-breeds', 'name': 'pokemon-breeds', 'autocomplete': 'on'}),
            'type1': forms.TextInput(attrs={'list': 'pokemon-types', 'name': 'pokemon-type1', 'autocomplete': 'on'}),
            'type2': forms.TextInput(attrs={'list': 'pokemon-types', 'name': 'pokemon-type2', 'autocomplete': 'on'}),
            'move1': forms.TextInput(attrs={'list': 'pokemon-moves', 'name': 'pokemon-moves', 'autocomplete': 'on'}),
            'move2': forms.TextInput(attrs={'list': 'pokemon-moves', 'name': 'pokemon-moves', 'autocomplete': 'on'}),
            'move3': forms.TextInput(attrs={'list': 'pokemon-moves', 'name': 'pokemon-moves', 'autocomplete': 'on'}),
            'move4': forms.TextInput(attrs={'list': 'pokemon-moves', 'name': 'pokemon-moves', 'autocomplete': 'on'}),
            'ability': forms.TextInput(attrs={'list': 'pokemon-abilities', 'name': 'pokemon-abilities', 'autocomplete': 'on'}),
            'nature': forms.TextInput(attrs={'list': 'pokemon-natures', 'name': 'pokemon-natures', 'autocomplete': 'on'}),
            'item': forms.TextInput(attrs={'list': 'pokemon-items', 'name': 'pokemon-items', 'autocomplete': 'on'}),
            'characteristic': forms.TextInput(attrs={'list': 'pokemon-characteristics', 'name': 'pokemon-characteristic', 'autocomplete': 'on'}),
        }
