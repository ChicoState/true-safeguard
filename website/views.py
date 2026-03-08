from django.shortcuts import render


def home(request):
    return render(request, 'website/home.html')

def apps(request):
    return render(request, 'website/apps.html')

def trends(request):
    return render(request, 'website/trends.html')

def blacklist(request):
    return render(request, 'website/blacklist.html')

def resources(request):
    return render(request, 'website/resources.html')