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
    path('admin/', admin.site.urls),
    path('webshop/', webshop, name='index'),
    path("webshop/<int:game_id>/", detail, name='detail'),
    path("webshop/signup/", signup, name='signup'),
    path("webshop/addgame/", addgame, name='addgame'),
    path('webshop/accounts/', include('django.contrib.auth.urls')),
    
    path('webshop/accounts/', include('allauth.urls')),
    

    
    
    path('webshop/profile/', profile, name='profile'),
    path('webshop/payment/', payment, name='payment'),
    path('activate/<uidb64>/<token>/', activate, name='activate' ),

    #url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
     #   views.activate, name='activate'),
    path('webshop/search/<str:search_text>', search_games, name='search'),
    path('webshop/edit_profile', edit_profile, name='edit_profile'),

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
