from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

def webshop(request):
    return HttpResponse("Hello, World")

def detail(request, game_id):
    return HttpResponse("<h2>Details for game_id" + str(game_id) + "</h2>")