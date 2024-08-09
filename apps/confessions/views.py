from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Confession
from .forms import ConfessionForm


@login_required
def confession_list(request):
    confessions = Confession.objects.filter(is_approved=True).order_by("-created_at")
    paginator = Paginator(confessions, 10)  # Show 10 confessions per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "confessions/confession_list.html", {"page_obj": page_obj})


@login_required
def submit_confession(request):
    if request.method == "POST":
        form = ConfessionForm(request.POST)
        if form.is_valid():
            confession = form.save(commit=False)
            confession.user = (
                request.user if not form.cleaned_data["anonymous"] else None
            )
            confession.save()
            messages.success(
                request, "Your confession has been submitted for approval."
            )
            return redirect("confessions:confession_list")
    else:
        form = ConfessionForm()
    return render(request, "confessions/submit_confession.html", {"form": form})


@user_passes_test(lambda u: u.is_staff)
def moderate_confessions(request):
    pending_confessions = Confession.objects.filter(is_approved=False)

    if request.method == "POST":
        confession_id = request.POST.get("confession_id")
        action = request.POST.get("action")

        confession = get_object_or_404(Confession, id=confession_id)
        if action == "approve":
            confession.is_approved = True
            confession.save()
            messages.success(request, f"Confession {confession.id} has been approved.")
        elif action == "reject":
            confession.delete()
            messages.success(
                request, f"Confession {confession.id} has been rejected and deleted."
            )

    return render(
        request,
        "confessions/moderate_confessions.html",
        {"confessions": pending_confessions},
    )
