from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.template import loader

from .models import Game

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