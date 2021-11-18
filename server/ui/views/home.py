from ui.view_tools import render_application

def home(request):
    return render_application(
        request, 
        scripts = ['/static/js-bundle/home.js'], 
        sub_title='home'
    )
