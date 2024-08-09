from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Q
from datetime import timedelta
from .models import Story, StoryView
from .forms import StoryForm
from django.db.models import Prefetch
from apps.accounts.models import User


@login_required
def create_story(request):
    if request.method == "POST":
        form = StoryForm(request.POST, request.FILES)
        if form.is_valid():
            story = form.save(commit=False)
            story.user = request.user
            story.expires_at = timezone.now() + timedelta(hours=24)
            story.save()
            return redirect("stories:view_stories")
    else:
        form = StoryForm()
    return render(request, "stories/create_story.html", {"form": form})


@login_required
def view_stories(request):
    current_time = timezone.now()
    query = request.GET.get("q")
    filter_type = request.GET.get("filter")

    active_stories = Story.objects.filter(expires_at__gt=current_time).order_by(
        "-created_at"
    )

    if query:
        active_stories = active_stories.filter(
            Q(user__username__icontains=query) | Q(caption__icontains=query)
        )

    if filter_type == "unviewed":
        viewed_stories = StoryView.objects.filter(viewer=request.user).values_list(
            "story", flat=True
        )
        active_stories = active_stories.exclude(id__in=viewed_stories)

    user_stories = get_grouped_active_stories(user=request.user)

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        # Return the auto-load stories template
        return render(
            request,
            "stories/auto_load_stories.html",
            {"users_with_stories": user_stories},
        )
    else:
        # Return the original view_stories template
        return render(
            request,
            "stories/view_stories.html",
            {"user_stories": user_stories, "query": query, "filter_type": filter_type},
        )


@login_required
def story_detail(request, story_id):
    story = get_object_or_404(Story, id=story_id)
    if story.is_expired():
        return redirect("stories:view_stories")

    StoryView.objects.get_or_create(story=story, viewer=request.user)

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return JsonResponse({"status": "success"})

    is_video = story.content.url.lower().endswith(".mp4")
    return render(
        request, "stories/story_detail.html", {"story": story, "is_video": is_video}
    )


@login_required
def user_stories(request, username):
    user = get_object_or_404(User, username=username)
    current_time = timezone.now()
    stories = Story.objects.filter(user=user, expires_at__gt=current_time).order_by(
        "created_at"
    )

    return render(
        request, "stories/user_stories.html", {"stories": stories, "story_user": user}
    )


def get_grouped_active_stories(user=None):
    current_time = timezone.now()
    active_stories = Story.objects.filter(expires_at__gt=current_time).order_by(
        "user", "-created_at"
    )

    if user:
        active_stories = active_stories.filter(user=user)

    # Group stories by user
    user_stories = {}
    for story in active_stories:
        if story.user not in user_stories:
            user_stories[story.user] = []
        user_stories[story.user].append(story)

    return user_stories


@login_required
def auto_load_stories(request):
    user_stories = get_grouped_active_stories()
    return render(
        request,
        "stories/auto_load_stories.html",
        {
            "users_with_stories": user_stories,
        },
    )

def get_all_stories(request):
    current_time = timezone.now()
    active_stories = Story.objects.filter(expires_at__gt=current_time).order_by(
        "user", "-created_at"
    )

    stories_data = []
    for story in active_stories:
        stories_data.append(
            {
                "id": story.id,
                "username": story.user.username,
                "user_avatar": (
                    story.user.profile_picture.url
                    if story.user.profile_picture
                    else None
                ),
                "content": story.content.url,
                "content_type": (
                    "video" if story.content.name.lower().endswith(".mp4") else "image"
                ),
                "caption": story.caption,
                "created_at": story.created_at.isoformat(),
            }
        )

    return JsonResponse({"stories": stories_data})
