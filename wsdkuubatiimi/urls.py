"""wsdkuubatiimi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from webshop.views import *
from webshop import views
from django.views.generic import TemplateView

urlpatterns = [
    path('', webshop, name='index'),
    path('/', webshop, name='index'),
    path('admin/', admin.site.urls),
    path('', webshop, name='index'),
    path("webshop/<int:game_id>/", detail, name='detail'),
    path("webshop/signup/", signup, name='signup'),
    path("webshop/addgame/", addgame, name='addgame'),
    path('webshop/accounts/', include('django.contrib.auth.urls')),
    path('webshop/accounts/', include('allauth.urls')),
    path('webshop/profile/', profile, name='profile'),

    #path('webshop/gameplay/', gameplay, name='gameplay'),   
    path('webshop/payment/', payment, name='payment'),

    path('webshop/edit_profile/', edit_profile, name='edit_profile'),
    path('webshop/update_dev/', update_dev, name='update_dev'),
    path('webshop/search/<str:search_text>', search_games, name='search'),

    
    path('activate/<uidb64>/<token>/', activate, name='activate' ),

    #Payment Urls
    path('webshop/payment/<game_id>/', payment, name='payment'),
    path('payment/error/', error, name='error'),
    path('payment/cancel/', cancel, name='cancel'),
    path('payment/success/', success, name='success'),
    path('payment/owned/', payment, name='payment'),


	#Modifying and removing a game
    path('webshop/your_games', your_games, name='your_games'),
    path('webshop/game<int:value>', game, name='game'),
    path('webshop/removegame/<int:value>',remove_game,name="remove_game"),
    
    
    path("webshop/savegame/", views.savegame, name='savegame'),
    path('webshop/loadgame/', views.loadgame, name='loadgame'),
    path('webshop/savescore/', views.savescore, name='savescore'),
    path('webshop/highscore/', views.highscore, name='highscore'),
]
handler404=chandler404
