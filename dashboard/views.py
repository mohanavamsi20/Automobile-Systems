from django.shortcuts import render, redirect

# Create your views here.
def render_home(request):
    if 'username' in request.session:
        template_name = 'dashboard/home.html'
        return render(request, template_name)
    return redirect('/login')