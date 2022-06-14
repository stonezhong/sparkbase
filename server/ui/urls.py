from django.urls import path
from django.shortcuts import render
from . import views

urlpatterns = [
    path('home',                views.home,                 name='home'),
    path('logout',              views.logout,               name='logout'),
    path('login',               views.login,                name='login'),
    path('privacy-policy',      lambda request: render(request, 'privacy_policy.html'))
]
