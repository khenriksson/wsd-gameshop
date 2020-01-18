from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.template import loader
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm

from .models import Game
from .forms import SignUpForm

# def webshop(request):
#      all_games = Game.objects.all()
#      html = ''
#      for game in all_games:
#         url = '/webshop/' + str(game.id) + '/'
#         html += '<a href="' + url + '">' + str(game.game_id) + '</a><br>'
#      return HttpResponse(html)

def navigation(request):
        return render(request, 'webshop/navigation.html')


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
            form.save()
            username = form.cleaned_data.get('username')
            #raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username) # insert password=raw_password here
            login(request, user)
            return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'webshop/signup.html', {'form': form})
        