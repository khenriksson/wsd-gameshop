from django.db import models
from django.conf import settings

# Create your models here.

class Game(models.Model):

    game_id = models.CharField(max_length=16)
    purchases = models.IntegerField()
    # developer = models.ForeignKey(User, on_delete=models.CASCADE)
    game_url = models.CharField(max_length=250)
    price = models.FloatField()
    def __str__(self):
        return self.game_id


class User(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    username = models.CharField(max_length=40)
    def __str__(self):
        return self.username
