from django.db import models
from django.conf import settings

# Create your models here.


class User(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    username = models.CharField(max_length=40)
    first_name = models.CharField(max_length=30, default="")
    last_name = models.CharField(max_length=30, default="")
    email = models.EmailField(max_length=254)
    def __str__(self):
        return self.username

# https://store-images.s-microsoft.com/image/apps.58949.14571142807322667.df9fc94b-3bd3-4ec2-b7a2-423331d84b17.5883e11e-8555-4114-83b7-72d1cb12cd6e?mode=scale&q=90&h=1080&w=1920
# Default picture for url
class Game(models.Model):
    purchases = models.IntegerField()
    #developer = models.ForeignKey(User, on_delete=models.CASCADE)
    game_url = models.URLField()
    picture_url = models.URLField(default="https://store-images.s-microsoft.com/image/apps.58949.14571142807322667.df9fc94b-3bd3-4ec2-b7a2-423331d84b17.5883e11e-8555-4114-83b7-72d1cb12cd6e?mode=scale&q=90&h=1080&w=1920")
    price = models.FloatField()
    game_title = models.CharField(max_length=50, default="Untitled")
    description = models.CharField(max_length=1000)
    def __str__(self):
        return self.game_title

class Wallet(models.Model):
    wallet_id = models.CharField(max_length=16, unique=True)  
    wallet_amount = models.FloatField(max_length=8)  
    owner = models.ForeignKey('User', on_delete=models.CASCADE)
    def __str__(self):
        return self.owner

class GameData(models.Model):
    game = models.ForeignKey('Game', on_delete=models.CASCADE, default=1)
    user = models.ForeignKey('User', on_delete=models.CASCADE, default=1)
    gameInfo = models.TextField()
    score = models.IntegerField(default = 0)
    


