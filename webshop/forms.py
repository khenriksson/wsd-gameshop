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
    game_id = forms.CharField(label='Game ID', max_length=16)
    purchases = forms.IntegerField(label='Purchases', initial='0')
    #developer = forms.ForeignKey(User)
    game_url = forms.URLField(label='Your game URL',initial='http://', required=True)
    price = forms.FloatField(label='Game price', required=False)
    game_title = forms.CharField(label='Game name', max_length=50, required=True)
        
    class Meta:
        model = Game
        fields = ('game_id', 'purchases', 'game_url','price','game_title')

        # widgets = {
        #     'game_id': form.TextInput(attrs={'class': 'form-control'}),
        #     'game_url': form.TextInput(attrs={'class': 'form-control'}),
        #     'price': form.TextInput(attrs={'class': 'form-control'}),
        #     'game_title': form.TextInput(attrs={'class': 'form-control'})
        # }