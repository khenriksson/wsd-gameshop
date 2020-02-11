from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Game
from allauth.account.forms import SignupForm




	
class SignUpForm(UserCreationForm):
    username = forms.CharField(label='Username', required=True)
    first_name = forms.CharField(label='First name', required=True)
    last_name = forms.CharField(label='Last name', required=True)
    email = forms.CharField(label="Email")
    group = forms.ChoiceField(choices = (
    ('Player', 'Player'),
    ('Developer', 'Developer'),),required = True, label = 'Sign up as:')
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
    game_url = forms.URLField(label='Your game URL', required=True)
    picture_url = forms.URLField(label='Your picture URL', required=False)
    price = forms.FloatField(label='Game price', required=False)
    game_title = forms.CharField(label='Game name', max_length=50, required=True)
    description = forms.CharField(label='Description', max_length=1000, required=False)
        
    class Meta:
        model = Game

        fields = ('game_title', 'game_url', 'picture_url', 'price')
##Form for Editing a game.
class EditGame(forms.ModelForm):	
    
    #fields = ('game_title', 'purchases', 'game_url', 'picture_url', 'price', 'description')


	game_title = forms.CharField(label='Game title',max_length=50)
	description = forms.CharField(label='Description',max_length=1000)
	
	game_url = forms.URLField(label='Game URL')
	picture_url = forms.URLField(label='Picture URL')
	price = forms.FloatField(label='Price of the game')

	class Meta:
		model= Game
		fields=('game_title','description','price','game_url','picture_url')
