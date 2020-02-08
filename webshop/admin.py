from django.contrib import admin
from .models import Game, User, Wallet, GameData, Transaction

# Register your models here.

admin.site.register(Game)
admin.site.register(GameData)
admin.site.register(Wallet)
admin.site.register(Transaction)
