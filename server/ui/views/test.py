from django.http  import HttpRequest, HttpResponse
from ui.view_tools import render_application

def test(request:HttpRequest)->HttpResponse:
    return render_application(
        request, 
        scripts = ['/static/js-bundle/test.js'], 
        sub_title='hello'
    )
