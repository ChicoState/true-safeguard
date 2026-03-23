from django.db import models

# Create your models here.
from django.shortcuts import render

def resources_view(request):
    # This mimics data you might eventually pull from a database
    context = {
        'categories': [
            {
                'title': 'Digital Wellbeing Tools',
                'description': 'Apps and extensions to help you monitor usage.',
                'links': [
                    {'name': 'Freedom', 'url': 'https://freedom.to', 'note': 'Block distracting sites across devices.'},
                    {'name': 'RescueTime', 'url': 'https://rescuetime.com', 'note': 'Automatic time tracking and reports.'},
                ]
            },
            {
                'title': 'Research & Articles',
                'description': 'Understand the science behind screen addiction.',
                'links': [
                    {'name': 'Center for Humane Tech', 'url': 'https://humanetech.com', 'note': 'Led by Tristan Harris.'},
                    {'name': 'Psychology Today: Screen Time', 'url': 'https://psychologytoday.com', 'note': 'Health impacts of blue light.'},
                ]
            }
        ]
    }
    return render(request, 'resources.html', context)