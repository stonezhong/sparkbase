from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, HttpResponseForbidden
import django.contrib.auth as auth
from django.urls import reverse
from ui.view_tools import render_application

def login(request:HttpRequest)->HttpResponse:
    if request.method == 'GET':
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('home'))

        auth_method = request.GET.get("auth", 'gmail')
        if auth_method == 'pwd':
            return render_application(
                request, 
                scripts = ['/static/js-bundle/login.js'], 
                sub_title='Login',
                init_menu_key="login"
            )

        if auth_method == 'gmail':
            return HttpResponseRedirect('/accounts/google/login/?process=login')

        return render_application(
            request, 
            scripts = ['/static/js-bundle/error.js'], 
            sub_title='Error',
            app_context={
                "subject": 403,
                "message": "Forbidden"
            },
            status=403
        )


    if request.method == 'POST':
        if request.user.is_authenticated:
            return render_application(
                request, 
                scripts = ['/static/js-bundle/error.js'], 
                sub_title='Error',
                app_context={
                    "subject": 403,
                    "message": "Forbidden"
                },
                status=403
            )

        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return HttpResponseRedirect(reverse('home'))

        # handle auth failure
        return render_application(
            request, 
            scripts = ['/static/js-bundle/login.js'], 
            sub_title='Login',
            app_context={
                "alert": {
                    "message": "Wrong username or password!",
                    "variant": "danger"
                }
            },
            init_menu_key="login"
        )
