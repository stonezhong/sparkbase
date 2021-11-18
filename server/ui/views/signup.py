import typing
import os
import json
from datetime import timedelta
from uuid import UUID
import urllib.parse
import jinja2
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden, Http404
from django.contrib.auth.models import User
from django.db import transaction
from main.models import AccessToken
from utils import send_email, get_config_json
from ui.view_tools import render_application, render_application_error



@transaction.atomic
def signup(request:HttpRequest)->HttpResponse:
    if request.method == 'GET':
        if request.user.is_authenticated:
            return render_application_error(
                request, 
                status=403,
                message="Forbidden"
            )

        return render_application(
            request, 
            scripts = ['/static/js-bundle/signup.js'], 
            sub_title='signup',
            init_menu_key="signup"
        )

    if request.method == 'POST':
        if request.user.is_authenticated:
            return HttpResponseForbidden("Please signout before signup!")

        username    = request.POST.get('username', '').strip()
        password    = request.POST.get('password', '').strip()
        password1   = request.POST.get('password1', '').strip()
        first_name  = request.POST.get('first_name', '').strip()
        last_name   = request.POST.get('last_name', '').strip()
        email       = request.POST.get('email', '').strip()

        can_signup = None
        msg_text = None

        # validate input
        while True:
            if len(username)==0:
                msg_text = "Username cannot be empty"
                break
            if len(password)==0:
                msg_text = "Password cannot be empty"
                break
            if len(password1)==0:
                msg_text = "Password cannot be empty"
                break
            if len(first_name)==0:
                msg_text = "First name cannot be empty"
                break
            if len(last_name)==0:
                msg_text = "Last name cannot be empty"
                break
            if len(email)==0:
                msg_text = "Email name cannot be empty"
                break
            if password != password1:
                msg_text = "Password does not match"
                break
            break
        if msg_text is not None:
            return render_application(
                request, 
                scripts = ['/static/js-bundle/signup.js'], 
                sub_title='signup',
                init_menu_key="signup",
                app_context = {
                    "alert": {
                        "message": msg_text,
                        "variant": "danger"
                    }
                }
            )


        user = find_user(username)
        if user is not None:
            can_signup = False
            msg_text = "Please try a different username!"
        else:
            token_key = f"signup-{username}"
            access_token = AccessToken.get(token_key)
            signup_info = {
                "username": username,
                "password": password,
                "first_name": first_name,
                "last_name": last_name,
                "email": email
            }
            if access_token is None:
                can_signup = True
                msg_text = f"An account validation email has been sent to {email}, please click the link in the email to validate your account"
                access_token = AccessToken.create(
                    token_key, signup_info, ttl=timedelta(hours=24)
                )
            else:
                # user already signed up with the last 24 hours
                # if they still use the same password, we allow user
                # to update info, especially maybe user just didn't get
                # our signup email
                token_signup_info = json.loads(access_token.content)
                if token_signup_info['password'] == password:
                    access_token.update_content(access_token)
                    can_signup = True
                    msg_text = "Please check you email to activate your account!"
                else:
                    can_signup = False
                    msg_text = "Please try a different username!"
        
        if not can_signup:
            return render_application(
                request, 
                scripts = ['/static/js-bundle/signup.js'], 
                sub_title='signup',
                init_menu_key="signup",
                app_context = {
                    "alert": {
                        "message": msg_text,
                        "variant": "danger"
                    }
                }
            )
        else:
            send_signup_validate_email(email=email, username=username, token_id=access_token.id)
            return render_application(
                request, 
                scripts = ['/static/js-bundle/signup.js'], 
                sub_title='signup',
                init_menu_key="signup",
                app_context = {
                    "alert": {
                        "message": "Please check you email and activate your account!",
                        "variant": "success"
                    }
                }
            )


def find_user(username:str)->typing.Optional[User]:
    users = User.objects.filter(username=username)
    if len(users) == 0:
        return None
    assert len(users) == 1
    return users[0]



def send_signup_validate_email(*, email:str, username:str, token_id:UUID)->None:
    app_config = get_config_json("config.json")
    base_url = app_config['base_url']
    url = os.path.join(base_url, "ui", "signup-validate") + "?" + urllib.parse.urlencode({
        'username': username,
        'token': str(token_id),
    })

    email_content = """\
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <link rel="stylesheet" href="style.css">
    <title>Data Manager Signup</title>
</head>
<body>
    <p>
    Hi {{username}}:
    </p>
    <p>
        Welcome to SparkBase! Please click the <a href="{{url}}">link here</a> to activate your account!
    </p>
</body>
</html>"""

    template = jinja2.Template(email_content)
    rendered_content = template.render({
        "url": url,
        "username": username
    })

    send_email(
        [email],
        "SparkBase: Please validate your account",
        "Please validate your account",
        rendered_content
    )

@transaction.atomic
def signup_validate(request:HttpRequest)->HttpResponse:
    if request.method != 'GET':
        return HttpResponseForbidden()
    
    access_token_id_str = request.GET['token']
    username = request.GET['username']

    try:
        access_token_id = UUID(access_token_id_str)
    except ValueError:
        raise Http404("Page not found!")
    
    try:
        access_token = AccessToken.objects.get(pk=access_token_id)
    except AccessToken.DoesNotExist:
        raise Http404("Page not found!")

    signup_info = json.loads(access_token.content)

    user = User.objects.create_user(
        username,
        email=signup_info['email'],
        password=signup_info['password'],
        first_name=signup_info['first_name'],
        last_name=signup_info['last_name'],
        is_active=True
    )
    user.save()
    access_token.delete()

    return render_application(
        request, 
        scripts = ['/static/js-bundle/login.js'], 
        sub_title='Login',
        app_context={
            "alert": {
                "message": "Your account has been validated, please login with your password!",
                "variant": "success"
            }
        },
        init_menu_key="login"
    )
