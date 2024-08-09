from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Event
from .forms import EventForm


@login_required
def create_event(request):
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.creator = request.user
            event.save()
            return redirect("events:event_detail", event_id=event.id)
    else:
        form = EventForm()
    return render(request, "events/create_event.html", {"form": form})


@login_required
def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    is_attending = request.user in event.attendees.all()
    return render(
        request,
        "events/event_detail.html",
        {"event": event, "is_attending": is_attending},
    )


@login_required
def event_list(request):
    query = request.GET.get("q", "").strip()
    start_date = request.GET.get("start_date", "")
    end_date = request.GET.get("end_date", "")

    events = Event.objects.all()

    if query:
        events = events.filter(title__icontains=query)

    if start_date:
        events = events.filter(start_time__gte=start_date)

    if end_date:
        events = events.filter(end_time__lte=end_date)

    events = events.order_by("start_time")

    return render(
        request,
        "events/event_list.html",
        {
            "events": events,
            "query": query,
            "start_date": start_date,
            "end_date": end_date,
        },
    )


@login_required
def attend_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    event.attendees.add(request.user)
    return redirect("events:event_detail", event_id=event.id)


@login_required
def unattend_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    event.attendees.remove(request.user)
    return redirect("events:event_detail", event_id=event.id)
