from django.shortcuts import render
from rest_framework.renderers import JSONRenderer

json_renderer = JSONRenderer()

def render_application(request, *, 
    scripts, sub_title, app_context=None, init_menu_key=None,
    status=200
):
    context={
        'user': request.user,
        'scripts': scripts,
        'sub_title': sub_title
    }

    if app_context is not None:
        context['app_context'] = json_renderer.render(app_context).decode("utf-8")
    
    if init_menu_key is not None:
        context['init_menu_key'] = init_menu_key

    return render(
        request,
        'application.html',
        context=context,
        status=status
    )

def render_application_error(request, *, status, message, subject=None):
    return render_application(
        request, 
        scripts = ['/static/js-bundle/error.js'], 
        sub_title='Error',
        app_context={
            "subject": subject or status,
            "message": message
        },
        status=status
    )

