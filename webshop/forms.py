from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Game

class SignUpForm(UserCreationForm):
    username = forms.CharField(label='Username')
        
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

class AddGameForm(forms.ModelForm):
    #game_id = forms.CharField(label='Game ID', max_length=16)
    purchases = forms.IntegerField(widget=forms.HiddenInput(), initial='0', required=False)
    #developer = forms.ForeignKey(User)
    game_url = forms.URLField(label='Your game URL',initial='http://', required=True)
    price = forms.FloatField(label='Game price', required=False)
    game_title = forms.CharField(label='Game name', max_length=50, required=True)
        
    class Meta:
        model = Game
        fields = ('game_title', 'purchases', 'game_url','price')

       