from django.shortcuts import render
from django.db.models import Q
from apps.feed.models import Post
from apps.groups.models import Group
from apps.events.models import Event
from apps.jobs.models import Job

def search(request):
    query = request.GET.get('q', '').strip()
    filter_type = request.GET.get('filter_type', 'all')

    if query:
        if filter_type == 'posts':
            posts = Post.objects.filter(Q(content__icontains=query))
            groups = Group.objects.none()
            events = Event.objects.none()
            jobs = Job.objects.none()
        elif filter_type == 'groups':
            posts = Post.objects.none()
            groups = Group.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
            events = Event.objects.none()
            jobs = Job.objects.none()
        elif filter_type == 'events':
            posts = Post.objects.none()
            groups = Group.objects.none()
            events = Event.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))
            jobs = Job.objects.none()
        elif filter_type == 'jobs':
            posts = Post.objects.none()
            groups = Group.objects.none()
            events = Event.objects.none()
            jobs = Job.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))
        else:  # 'all'
            posts = Post.objects.filter(Q(content__icontains=query))
            groups = Group.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
            events = Event.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))
            jobs = Job.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))
    else:
        posts = Post.objects.none()
        groups = Group.objects.none()
        events = Event.objects.none()
        jobs = Job.objects.none()

    context = {
        'query': query,
        'filter_type': filter_type,
        'posts': posts,
        'groups': groups,
        'events': events,
        'jobs': jobs,
    }
    return render(request, 'search/search_results.html', context)
