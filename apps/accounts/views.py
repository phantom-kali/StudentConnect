from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, render, redirect
from django.core.mail import send_mail
from django.conf import settings

from apps.accounts.models import User
from .forms import UserRegistrationForm, UserLoginForm, UserProfileForm
from apps.feed.models import Post
from django.db.models import Q
from django.core.paginator import Paginator
from django.db.models import Count
import random
import string

User = get_user_model()


def generate_password():
    return "".join(random.choices(string.ascii_letters + string.digits, k=10))


@login_required
def referral_program(request):
    return render(request, "accounts/referral_program.html")


@login_required
def home(request):
    return render(request, "accounts/home.html")


def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            referral_code = form.cleaned_data.get("referral_code")
            if referral_code:
                try:
                    referrer = User.objects.get(referral_code=referral_code)
                    user.referred_by = referrer
                except User.DoesNotExist:
                    form.add_error("referral_code", "Invalid referral code")
                    return render(request, "accounts/register.html", {"form": form})
            user.save()
            if referral_code and referrer:
                referrer.add_referral(user)
            login(request, user)
            return redirect("feed:index")
    else:
        form = UserRegistrationForm()
    return render(request, "accounts/register.html", {"form": form})


def user_login(request):
    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = authenticate(request, email=email, password=password)
            if user:
                login(request, user)
                next_url = request.GET.get("next")
                if next_url:
                    return redirect(next_url)
                return redirect("feed:index")
    else:
        form = UserLoginForm()
    return render(request, "accounts/login.html", {"form": form})


@login_required
def profile(request, user_id=None):
    if user_id:
        user = get_object_or_404(User, id=user_id)
        is_own_profile = user == request.user
    else:
        user = request.user
        is_own_profile = True

    if request.method == "POST" and is_own_profile:
        form = UserProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect("accounts:profile", user_id=user.id)
    else:
        form = UserProfileForm(instance=user) if is_own_profile else None

    followers = user.followers.all()
    following = user.following.all()
    posts = Post.objects.filter(user=user).order_by("-created_at")

    context = {
        "profile_user": user,
        "form": form,
        "is_own_profile": is_own_profile,
        "followers": followers,
        "following": following,
        "posts": posts,
        "followers_count": followers.count(),
        "following_count": following.count(),
        "posts_count": posts.count(),
    }
    return render(request, "accounts/profile.html", context)


@login_required
def followers_list(request, user_id):
    user = get_object_or_404(User, id=user_id)
    followers = user.followers.all().order_by("username")  # Add ordering
    paginator = Paginator(followers, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
        "profile_user": user,
        "page_obj": page_obj,
        "followers_count": followers.count(),
    }
    return render(request, "accounts/followers_list.html", context)


@login_required
def following_list(request, user_id):
    user = get_object_or_404(User, id=user_id)
    following = user.following.all().order_by("username")
    paginator = Paginator(following, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
        "profile_user": user,
        "page_obj": page_obj,
        "following_count": following.count(),
    }
    return render(request, "accounts/following_list.html", context)


@login_required
def posts_list(request, user_id):
    user = get_object_or_404(User, id=user_id)
    posts = Post.objects.filter(user=user).order_by("-created_at")
    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
        "profile_user": user,
        "page_obj": page_obj,
        "posts_count": posts.count(),
    }
    return render(request, "accounts/posts_list.html", context)


@login_required
def follow_user(request, username):
    user_to_follow = get_object_or_404(User, username=username)
    request.user.following.add(user_to_follow)
    return redirect("accounts:profile", user_id=user_to_follow.id)


@login_required
def unfollow_user(request, username):
    user_to_unfollow = get_object_or_404(User, username=username)
    request.user.following.remove(user_to_unfollow)
    return redirect("accounts:profile", user_id=user_to_unfollow.id)


@login_required
def user_logout(request):
    logout(request)
    return redirect("accounts:login")


def password_reset(request):
    if request.method == "POST":
        email = request.POST.get("email")
        try:
            user = User.objects.get(email=email)
            new_password = generate_password()
            user.set_password(new_password)
            user.save()

            send_mail(
                "Password Reset",
                f"Your new password is: {new_password}",
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
            return redirect("accounts:login")
        except User.DoesNotExist:
            # Handle case where user doesn't exist
            pass
    return render(request, "accounts/password_reset.html")
