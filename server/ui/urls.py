from django.urls import path
from . import views

urlpatterns = [
    path('home',                views.home,                 name='home'),
    path('test',                views.test,                 name='test'),
    path('logout',              views.logout,               name='logout'),
    path('login',               views.login,                name='login'),
    path('signup',              views.signup,               name='signup'),
    path('signup-validate',     views.signup_validate,      name='signup-validate'),
]
