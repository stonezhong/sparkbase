from ui.view_tools import render_application

def test(request):
    return render_application(
        request, 
        scripts = ['/static/js-bundle/test.js'], 
        sub_title='hello'
    )
