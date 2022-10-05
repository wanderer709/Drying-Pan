from django.contrib import admin
from .models import Team, Pokemon
# from .forms import TeamCreateForm

# class TeamAdmin(admin.ModelAdmin):
#     form = TeamCreateForm

admin.site.register(Team)
admin.site.register(Pokemon)

