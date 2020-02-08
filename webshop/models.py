from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

from hashlib import md5


import datetime
# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    username = models.CharField(max_length=40)
    first_name = models.CharField(max_length=30, default="")
    last_name = models.CharField(max_length=30, default="")
    email = models.EmailField(max_length=254)

    def __str__(self):
        return self.user.username

# https://store-images.s-microsoft.com/image/apps.58949.14571142807322667.df9fc94b-3bd3-4ec2-b7a2-423331d84b17.5883e11e-8555-4114-83b7-72d1cb12cd6e?mode=scale&q=90&h=1080&w=1920
# Default picture for url
class Game(models.Model):
    purchases = models.IntegerField()
    developer = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    game_url = models.URLField()
    picture_url = models.URLField(default="https://store-images.s-microsoft.com/image/apps.58949.14571142807322667.df9fc94b-3bd3-4ec2-b7a2-423331d84b17.5883e11e-8555-4114-83b7-72d1cb12cd6e?mode=scale&q=90&h=1080&w=1920", blank=True)
    price = models.DecimalField(decimal_places=2, max_digits=8) # Needs to be decimalfield
    game_title = models.CharField(max_length=50, default="Untitled")
    description = models.CharField(max_length=1000, default="")
    times_bought = models.PositiveIntegerField(default = 0)

    def __str__(self):
        return self.game_title

class Wallet(models.Model):
    wallet_id = models.CharField(max_length=16, unique=True)  
    wallet_amount = models.FloatField(max_length=8)  
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.owner

class GameData(models.Model):
    game = models.IntegerField()
    user = models.TextField()
    gameInfo = models.TextField()
    score = models.IntegerField(default = 0)
    
class Transaction(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    state = models.CharField(max_length=20, default="Pending")
    buy_started = models.DateTimeField(default=datetime.datetime.now, blank=True)
    buy_completed = models.DateTimeField(null=True)
    pid = models.CharField(blank=True, max_length=64)

    class Meta:
        unique_together = ('game', 'buyer')

    def __str__(self):
        return self.buyer.username

