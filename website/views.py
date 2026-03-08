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
    resource_data = resource_data = [
        {
            'category_name': 'Recognizing Screen Fatigue & Overstimulation',
            'category_info': 'Parents often miss the early signs of screen fatigue because they look like regular tiredness. Watch for the "Tired but Wired" state—where a child is clearly exhausted but physically unable to calm down. Ask yourself: Is my child often angry or irritable? Does it seem like they are always having a hard time? Excessive screen time could be the culprit.',
            'links': [
            {
                'title': 'The "Physical 5" Checklist', 
                'url': 'https://www.healthychildren.org/English/health-issues/conditions/eyes/Pages/What-Too-Much-Screen-Time-Does-to-Your-Childs-Eyes.aspx', 
                'desc': 'Check for: 1. Excessive eye rubbing, 2. Dilated pupils, 3. Rapid blinking, 4. Head tilting/squinting, and 5. Unusual clumsiness after playing.'
            },
            {
                'title': 'Behavioral Red Flags', 
                'url': 'https://socalmentalwellness.com/child-counseling/too-much-screen-time/', 
                'desc': 'Look for "Screen Crashes": intense irritability, aggression, or a "glazed over" look where the child doesn\'t respond to their name.'
            },
    ]
        },
        {
            'category_name': 'Detecting AI & Synthetic Media',
            'category_info': 'In an era of deepfakes, children must be taught to verify the authenticity of what they see. We recommend the "SIFT" method: Stop, Investigate the source, Find better coverage, and Trace claims back to the original context.',
            'links': [
                {'title': 'Spotting Deepfakes', 'url': 'https://www.mit.edu', 'desc': 'Key visual markers to identify AI-generated faces and voices.'},
                {'title': 'Fact-Checking for Kids', 'url': 'https://www.commonsensemedia.org', 'desc': 'Tools to help children distinguish between real footage and synthetic media.'},
            ]
        },
        {
            'category_name': 'Evidence-Based Alternatives',
            'category_info': 'Replacing screen time is most effective when the alternative provides similar cognitive engagement. Low-dopamine activities allow the brain to reset and improve sustained attention spans.',
            'links': [
                {'title': 'Open-Ended Play Resources', 'url': 'https://www.naeyc.org', 'desc': 'Research on how tactile play builds executive function better than apps.'},
                {'title': 'Screen-Free Week Toolkits', 'url': 'https://www.screenfree.org', 'desc': 'Practical planners for transitioning families to a lower-tech lifestyle.'},
            ]
        },
        {
            'category_name': 'Local Spotlight: Chico Area Recreation & Park District (CARD)',
            'category_info': 'For those in the Chico area, CARD provides vital screen-free outlets. From the Chico Creek Nature Center to specialized youth clubs, these programs focus on physical health and outdoor skill-building.',
        'links': [
            {'title': 'CARD Official Website', 'url': 'https://www.chicorec.gov/', 'desc': 'Explore the full catalog of sports, martial arts, and community classes.'},
            {'title': 'Park Explorers Survival Club', 'url': 'https://www.chicorec.gov/park-explorers-survival-club', 'desc': 'Outdoor adventures uncovering hidden trails and learning wilderness survival skills.'},
            {'title': 'Chico Creek Nature Center', 'url': 'https://www.chicorec.gov/chico-creek-nature-center', 'desc': 'Nature ABCs, night hikes, and spring/summer camps located in Bidwell Park.'},
        ]
        }
    ]

    return render(request, 'website/resources.html', {'categories': resource_data})

