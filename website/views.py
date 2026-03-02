from django.shortcuts import render


def home(request):
    return render(request, 'website/home.html')


def blacklist(request):
    return render(request, 'website/blacklist.html')
