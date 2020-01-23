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

urlpatterns = [
    path('admin/', admin.site.urls),
    path('webshop/', webshop, name='index'),
    path("webshop/<int:game_id>/", detail, name='detail'),
    path("webshop/signup/", signup, name='signup'),
    path("webshop/addgame/", addgame, name='addgame'),
    path('webshop/accounts/', include('django.contrib.auth.urls')),
    path('webshop/profile/', profile, name='profile'),
    path('webshop/gameplay/', gameplay, name='gameplay'),
    path('webshop/payment/', payment, name='payment')
]
