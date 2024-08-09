from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post, Comment, Report, ReportOption
from django.http import JsonResponse
from .forms import PostForm, CommentForm
from .models import Post
from django.db.models import Count
from django.utils import timezone


@login_required
def feed(request):
    posts_list = Post.objects.all()
    paginator = Paginator(posts_list, 10)  # Show 10 posts per page

    page = request.GET.get("page")
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            form.save_m2m()  # Save tags
            return redirect("feed:index")
    else:
        form = PostForm()
    return render(request, "feed/feed.html", {"posts": posts, "form": form})


@login_required
def post_detail(request, post_id):
    post = Post.objects.get(id=post_id)
    post.increment_view_count()
    comments = post.comments.all()
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
            return redirect("feed:post_detail", post_id=post.id)
    else:
        form = CommentForm()
    return render(
        request,
        "feed/post_detail.html",
        {"post": post, "comments": comments, "form": form},
    )


@login_required
def recommended_posts(request):
    user = request.user
    user_interests = (
        Post.objects.filter(likes__user=user)
        .values("tags__name")
        .annotate(count=Count("tags__name"))
        .order_by("-count")[:5]
    )

    recommended_list = (
        Post.objects.filter(
            tags__name__in=user_interests.values_list("tags__name", flat=True)
        )
        .exclude(views__user=user)
        .distinct()
        .order_by("-created_at")
    )

    paginator = Paginator(recommended_list, 10)  # Show 10 posts per page
    page = request.GET.get("page")
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, "feed/recommended_posts.html", {"posts": posts})


@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return redirect("feed:post_detail", post_id=post.id)


@login_required
def report_post(request, post_id):
    if request.method == "POST":
        post = get_object_or_404(Post, id=post_id)
        reason = request.POST.get("reason")
        Report.objects.create(user=request.user, post=post, reason=reason)
        if request.is_ajax():
            return JsonResponse({"status": "success"})
        messages.success(request, "Post reported successfully.")
    return redirect("feed:post_detail", post_id=post_id)


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user == post.user:
        post.delete()
        messages.success(request, "Post deleted successfully.")
    else:
        messages.error(request, "You don't have permission to delete this post.")
    return redirect("feed:index")


@login_required
def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            form.save_m2m()  # Save tags
            return redirect("feed:post_detail", post_id=post.id)
    else:
        form = PostForm()
    return render(request, "feed/create_post.html", {"form": form})


@login_required
def following_feed(request):
    following_users = request.user.following.all()
    posts = Post.objects.filter(user__in=following_users).order_by("-created_at")
    return render(request, "feed/feed.html", {"posts": posts, "feed_type": "following"})


@login_required
def trending_feed(request):
    # Get posts from the last 7 days
    last_week = timezone.now() - timezone.timedelta(days=7)
    trending_posts = (
        Post.objects.filter(created_at__gte=last_week)
        .annotate(like_count=Count("likes"))
        .order_by("-like_count", "-created_at")[:20]
    )
    return render(
        request, "feed/feed.html", {"posts": trending_posts, "feed_type": "trending"}
    )
