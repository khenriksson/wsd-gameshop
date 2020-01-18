from django.db import models
from django.conf import settings

# Create your models here.


class User(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    username = models.CharField(max_length=40)
    def __str__(self):
        return self.username

class Game(models.Model):

    game_id = models.CharField(max_length=16)
    purchases = models.IntegerField()
    #developer = models.ForeignKey(User, on_delete=models.CASCADE)
    game_url = models.URLField()
    price = models.FloatField()
    game_title = models.CharField(max_length=50, default="Untitled")
    def __str__(self):
        return self.game_id

class Wallet(models.Model):
    wallet_id = models.CharField(max_length=16, unique=True)  
    wallet_amount = models.FloatField(max_length=8)  
    owner = models.ForeignKey('User', on_delete=models.CASCADE)
    def __str__(self):
        return self.owner


