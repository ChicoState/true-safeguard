from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import JsonResponse
from .models import BlacklistItem, ForumPost, PostVote, Comment, Profile, Notification

def home(request):
    return render(request, 'website/home.html')

def apps(request):
    return render(request, 'website/apps.html')

def trends(request):
    return render(request, 'website/trends.html')

def blacklist(request):
    blacklist_items = BlacklistItem.objects.all()
    return render(request, 'website/blacklist.html', {'blacklist_items': blacklist_items})

def resources(request):
    resource_data = [
        {
            'category_name': 'Recognizing Screen Fatigue & Overstimulation',
            'category_info': 'Parents often miss the early signs of screen fatigue because they look like regular tiredness.',
            'links': []
        }
    ]
    return render(request, 'website/resources.html', {'categories': resource_data})

def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return render(request, "website/register.html")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return render(request, "website/register.html")

        try:
            validate_password(password1)
        except ValidationError as e:
            for error in e.messages:
                messages.error(request, error)
            return render(request, "website/register.html")

        user = User.objects.create_user(username=username, password=password1)
        user.save()

        messages.success(request, "Account created successfully.")
        return redirect("login")

    return render(request, "website/register.html")

def login_view(request):
    return render(request, "website/login.html")

def forum(request):
    selected_category = request.GET.get("category")
    categories = ["Games", "Apps", "Trends", "Movies", "Advice"]

    posts = ForumPost.objects.all()

    if selected_category in categories:
        posts = posts.filter(category=selected_category)

    return render(request, 'website/forum.html', {
        'posts': posts,
        'categories': categories,
        'selected_category': selected_category,
    })

def profile_detail(request, username):
    profile_user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=profile_user)
    posts = ForumPost.objects.filter(author=profile_user)

    is_following = False
    if request.user.is_authenticated:
        is_following = profile.followers.filter(id=request.user.id).exists()

    return render(request, "website/profile.html", {
        "profile_user": profile_user,
        "profile": profile,
        "posts": posts,
        "is_following": is_following,
    })

@login_required
def follow_user(request, username):
    profile_user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=profile_user)

    if profile_user == request.user:
        messages.error(request, "You cannot follow yourself.")
        return redirect("profile_detail", username=username)

    if profile.followers.filter(id=request.user.id).exists():
        profile.followers.remove(request.user)
    else:
        profile.followers.add(request.user)
        Notification.objects.create(
            user=profile_user,
            message=f"{request.user.username} followed you."
        )

    return redirect("profile_detail", username=username)

@login_required
def create_post(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        category = request.POST.get("category")

        post = ForumPost.objects.create(
            author=request.user,
            title=title,
            content=content,
            category=category
        )

        profile = get_object_or_404(Profile, user=request.user)

        for follower in profile.followers.all():
            Notification.objects.create(
                user=follower,
                message=f"{request.user.username} created a new post: {post.title}"
            )

        return redirect("forum")

    return render(request, "website/create_post.html")

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(ForumPost, id=post_id)

    if post.author != request.user:
        messages.error(request, "You can only delete your own posts.")
        return redirect("forum")

    if request.method == "POST":
        post.delete()
        messages.success(request, "Post deleted.")
        return redirect("forum")

    return redirect("forum")

@login_required
def vote_post(request, post_id, vote_value):
    post = get_object_or_404(ForumPost, id=post_id)

    if vote_value == 0:
        vote_value = -1

    vote, created = PostVote.objects.get_or_create(
        user=request.user,
        post=post,
        defaults={"value": vote_value}
    )

    if not created:
        if vote.value == vote_value:
            vote.delete()
        else:
            vote.value = vote_value
            vote.save()

    return redirect("forum")

@login_required
def add_comment(request, post_id):
    post = get_object_or_404(ForumPost, id=post_id)

    if request.method == "POST":
        content = request.POST.get("content")

        if content:
            Comment.objects.create(
                author=request.user,
                post=post,
                content=content
            )

    return redirect("forum")

@login_required
def edit_post(request, post_id):
    post = get_object_or_404(ForumPost, id=post_id)

    if post.author != request.user:
        return redirect("forum")

    if request.method == "POST":
        post.title = request.POST.get("title")
        post.content = request.POST.get("content")
        post.category = request.POST.get("category")
        post.edited_at = timezone.now()
        post.save()

        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return JsonResponse({
                "title": post.title,
                "content": post.content,
                "category": post.category,
                "meta": f'Edited by <a href="/profile/{post.author.username}/">{post.author.username}</a> on {post.edited_at}'
            })

        return redirect("forum")

    return render(request, "website/edit_post.html", {"post": post})

@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if comment.author != request.user:
        return redirect("forum")

    if request.method == "POST":
        comment.content = request.POST.get("content")
        comment.edited_at = timezone.now()
        comment.save()

        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return JsonResponse({
                "content": comment.content,
                "meta": f'Edited by <a href="/profile/{comment.author.username}/">{comment.author.username}</a> on {comment.edited_at}'
            })

        return redirect("forum")

    return render(request, "website/edit_comment.html", {"comment": comment})

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if comment.author != request.user:
        return redirect("forum")

    if request.method == "POST":
        comment.delete()
        messages.success(request, "Comment deleted.")

    return redirect("forum")

@login_required
def edit_bio(request):
    profile = get_object_or_404(Profile, user=request.user)

    if request.method == "POST":
        profile.bio = request.POST.get("bio")
        profile.save()
        messages.success(request, "Bio updated.")

    return redirect("profile_detail", username=request.user.username)

@login_required
def notifications(request):
    user_notifications = request.user.notifications.all()
    return render(request, "website/notifications.html", {
        "notifications": user_notifications
    })