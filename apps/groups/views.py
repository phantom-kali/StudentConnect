from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Group, GroupPost
from .forms import GroupForm, GroupPostForm


@login_required
def create_group(request):
    if request.method == "POST":
        form = GroupForm(request.POST)
        if form.is_valid():
            group = form.save()
            group.members.add(request.user)
            return redirect("groups:group_detail", group_id=group.id)
    else:
        form = GroupForm()
    return render(request, "groups/create_group.html", {"form": form})


@login_required
def group_detail(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    posts = group.posts.all()
    if request.method == "POST":
        form = GroupPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.group = group
            post.user = request.user
            post.save()
            return redirect("groups:group_detail", group_id=group.id)
    else:
        form = GroupPostForm()
    return render(
        request,
        "groups/group_detail.html",
        {"group": group, "posts": posts, "form": form},
    )


@login_required
def join_group(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    group.members.add(request.user)
    return redirect("groups:group_detail", group_id=group.id)


@login_required
def leave_group(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    group.members.remove(request.user)
    return redirect("groups:group_list")


@login_required
def group_list(request):
    query = request.GET.get("q", "").strip()
    groups = Group.objects.all()

    if query:
        groups = groups.filter(name__icontains=query)

    return render(request, "groups/group_list.html", {"groups": groups, "query": query})
