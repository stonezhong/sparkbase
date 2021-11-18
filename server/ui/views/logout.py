from django.http import  HttpResponseRedirect
from django.urls import reverse
import django.contrib.auth as auth

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('login'))
