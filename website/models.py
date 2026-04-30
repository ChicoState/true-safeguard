from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


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


class BlacklistItem(models.Model):
    """Model for apps, games, websites that may not be age-appropriate."""
    
    CATEGORY_CHOICES = [
        ('Apps', 'Apps'),
        ('Games', 'Games'),
        ('Social Media', 'Social Media'),
        ('Websites', 'Websites'),
    ]
    
    AGE_GROUP_CHOICES = [
        ('Toddlers', 'Toddlers'),
        ('Elementary', 'Elementary'),
        ('Middle School', 'Middle School'),
        ('Teens', 'Teens'),
    ]
    
    RISK_LEVEL_CHOICES = [
        ('High', 'High'),
        ('Medium', 'Medium'),
        ('Low', 'Low'),
    ]
    
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    age_group = models.CharField(max_length=50, choices=AGE_GROUP_CHOICES)
    risk_level = models.CharField(max_length=20, choices=RISK_LEVEL_CHOICES)
    short_description = models.TextField()
    flagged_reasons = models.JSONField(default=list, help_text="List of reasons why this item is flagged")
    parent_tips = models.JSONField(default=list, help_text="List of tips for parents")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-risk_level', 'name']
    
    def __str__(self):
        return f"{self.name} ({self.risk_level} Risk)"
    
class ForumPost(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
    
    def vote_score(self):
        return sum(vote.value for vote in self.votes.all())
    
class PostVote(models.Model):
    VOTE_CHOICES = [
        (1, 'Upvote'),
        (-1, 'Downvote'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(ForumPost, on_delete=models.CASCADE, related_name='votes')
    value = models.IntegerField(choices=VOTE_CHOICES)

    class Meta:
        unique_together = ('user', 'post')

    def __str__(self):
        return f"{self.user.username} voted {self.value} on {self.post.title}"
    
class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(ForumPost, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.title}"
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    followers = models.ManyToManyField(
        User,
        related_name='following',
        blank=True
    )

    def __str__(self):
        return self.user.username

    def follower_count(self):
        return self.followers.count()


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.message

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)