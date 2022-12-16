from django.shortcuts import render, redirect


def index(request):
    if request.user.is_authenticated:
        return redirect("/dashboard")
    else:
        return render(request, 'index.html', {})


def settings(request):
    settings_list = request.META
    return render(request, 'debug/settings.html', {'settings': settings_list})


def superadmin(request):
    print 
    if request.META.get('REMOTE_ADDR') == "127.0.0.1":
        return render(request, 'superadmin.html', {})
    else:
        return redirect('/')

