from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.urls import reverse
import django.contrib.auth as auth

def logout(request:HttpRequest)->HttpResponse:
    auth.logout(request)
    return HttpResponseRedirect(reverse('login'))
