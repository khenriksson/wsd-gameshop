from django.contrib import admin
from .models import Game, User, GameData

# Register your models here.

admin.site.register(Game)
admin.site.register(GameData)