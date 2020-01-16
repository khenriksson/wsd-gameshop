from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404


def webshop(request):
        return HttpResponse("Hello, World")