from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Game

class SignUpForm(UserCreationForm):
    username = forms.CharField(label='Username', required=True)
    first_name = forms.CharField(label='First name', required=True)
    last_name = forms.CharField(label='Last name', required=True)
    email = forms.CharField(label="Email")
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

class EditProfileForm(forms.ModelForm):
    first_name = forms.CharField(label='First Name')
    last_name = forms.CharField(label='Last Name')
    email = forms.CharField(label="Email")
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class AddGameForm(forms.ModelForm):
    purchases = forms.IntegerField(widget=forms.HiddenInput(), initial='0', required=False)
    game_url = forms.URLField(label='Your game URL',initial='http://', required=True)
    picture_url = forms.URLField(label='Your picture URL',initial='http://', required=False)
    price = forms.FloatField(label='Game price', required=False)
    game_title = forms.CharField(label='Game name', max_length=50, required=True)
    description = forms.CharField(label='description', initial="", max_length=1000)
        
    class Meta:
        model = Game
        fields = ('game_title', 'purchases', 'game_url', 'picture_url', 'price')

       