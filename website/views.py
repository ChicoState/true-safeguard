from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

def home(request):
    return render(request, 'website/home.html')

def apps(request):
    return render(request, 'website/apps.html')

def trends(request):
    return render(request, 'website/trends.html')

def blacklist(request):
    return render(request, 'website/blacklist.html')

def resources(request):
    categories = [
        {
            'category_name': 'Recognizing Screen Fatigue & Overstimulation',
            'category_info': 'Parents often miss the early signs of screen fatigue...',
            'links': [
                {
                    'title': 'The "Physical 5" Checklist', 
                    'url': 'https://www.healthychildren.org/...', 
                    'desc': 'Check for: 1. Excessive eye rubbing, 2. Dilated pupils...'
                },
                {
                    'title': 'Behavioral Red Flags', 
                    'url': 'https://socalmentalwellness.com/...', 
                    'desc': 'Look for "Screen Crashes": intense irritability...'
                },
            ]
        },
        {
            'category_name': 'Detecting AI & Synthetic Media',
            'category_info': 'In an era of deepfakes...',
            'links': [
                {'title': 'Spotting Deepfakes', 'url': 'https://www.mit.edu', 'desc': 'Key visual markers...'},
                {'title': 'Fact-Checking for Kids', 'url': 'https://www.commonsensemedia.org', 'desc': 'Tools to help children...'},
            ]
        },
        {
            'category_name': 'Evidence-Based Alternatives',
            'category_info': 'Replacing screen time is most effective...',
            'links': [
                {'title': 'Open-Ended Play Resources', 'url': 'https://www.naeyc.org', 'desc': 'Research on tactile play...'},
                {'title': 'Screen-Free Week Toolkits', 'url': 'https://www.screenfree.org', 'desc': 'Practical planners...'},
            ]
        },
        {
            'category_name': 'Local Spotlight: Chico Area Recreation & Park District (CARD)',
            'category_info': 'For those in the Chico area, CARD provides vital screen-free outlets...',
            'links': [
                {'title': 'CARD Official Website', 'url': 'https://www.chicorec.gov/', 'desc': 'Explore the full catalog...'},
                {'title': 'Park Explorers Survival Club', 'url': 'https://www.chicorec.gov/...', 'desc': 'Outdoor adventures...'},
                {'title': 'Chico Creek Nature Center', 'url': 'https://www.chicorec.gov/...', 'desc': 'Nature ABCs...'},
            ]
        } # Removed the rogue 'offline_activities' from inside this list
    ]
    
    offline_activities = [
        {'title': 'Chess & Strategy', 'desc': 'Builds patience and long-term planning skills.'},
        {'title': 'Jigsaw Puzzles', 'desc': 'Great for tactile pattern recognition and family bonding.'},
        {'title': 'Shared Reading', 'desc': 'Reduces stress and improves vocabulary away from blue light.'},
        {'title': 'Butte County Library', 'desc': 'Visit the Chico branch for storytime and free book rentals.'},
    ]

    context = {
        'categories': categories,
        'offline_activities': offline_activities
    }

    return render(request, 'website/resources.html', context)

def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        # 1. Passwords must match
        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return render(request, "website/register.html")

        # 2. Username must be unique
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return render(request, "website/register.html")

        # 3. Run Django's password validators
        try:
            validate_password(password1)
        except ValidationError as e:
            for error in e.messages:
                messages.error(request, error)
            return render(request, "website/register.html")

        # 4. Create the user
        user = User.objects.create_user(username=username, password=password1)
        user.save()

        messages.success(request, "Account created successfully. Please log in.")
        return redirect("login")

    return render(request, "website/register.html")