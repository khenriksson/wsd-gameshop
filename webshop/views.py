from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.template import loader
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.core.mail import BadHeaderError, send_mail

from .models import Game, User
from .forms import SignUpForm, AddGameForm

def webshop(request):
    all_games = Game.objects.all()
    template = loader.get_template('webshop/index.html')
    context = {
        'all_games': all_games,
    }
    return HttpResponse(template.render(context, request))

def detail(request, game_id):
    try:
        game = Game.objects.get(pk=game_id)
    except Game.DoesNotExist:
        raise Http404("Game does not exist")
    return render(request, 'webshop/detail.html', {'game': game})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            send_email(request, user.email)
            return redirect('index')
            
    else:
        form = SignUpForm()
    return render(request, 'webshop/signup.html', {'form': form})
    

def addgame(request):
    if request.user.is_authenticated:
        game = Game()
        if request.method == 'POST':
            form = AddGameForm(request.POST)
            if form.is_valid():
                game = form.save(commit = False)
                game.save()
                return redirect('index')
            
        else:
            form = AddGameForm()
        return render(request, 'webshop/addgame.html', {'form': form})
    else: return redirect('index')

def profile(request):
    return render(request, 'webshop/profile.html')
def gameplay(request):
    #return TemplateResponse(request, 'webshop/game.html', {'redirect_url':'https://www.google.com/url?q=https://users.aalto.fi/~oseppala/game/example_game.html&sa=D&ust=1579184818170000'}
    return render(request, 'webshop/gameplay.html')



# A secure way of sending the registered emails
def send_email(request, user_email):
    try:
        # No way to do header injections
        subject = request.POST.get('subject', 'Welcome to Kuubatiimi Gameshop')
        message = request.POST.get('message', 'Now go buy some games!')
        from_email = request.POST.get('from_email', 'noreply@kuubatiimi.com')
        if subject and message and from_email:
            try:
                send_mail(subject, message, from_email, [user_email])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('index')
        else:
            return HttpResponse('Make sure all fields are entered and valid.')
    except User.DoesNotExist:
        raise Http404("User does not exist")
    
        