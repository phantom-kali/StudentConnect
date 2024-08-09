from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.urls import reverse
from .models import Job, Application
from .forms import JobFilterForm, JobForm, ApplicationForm
from apps.messaging.models import Conversation, Message
from apps.notifications.models import Notification


@login_required
def job_list(request):
    jobs = Job.objects.all()
    form = JobFilterForm(request.GET)

    if form.is_valid():
        title = form.cleaned_data.get("title")
        company = form.cleaned_data.get("company")
        location = form.cleaned_data.get("location")
        status = form.cleaned_data.get("status")
        sort_by = form.cleaned_data.get("sort_by")

        if title:
            jobs = jobs.filter(title__icontains=title)
        if company:
            jobs = jobs.filter(company__icontains=company)
        if location:
            jobs = jobs.filter(location__icontains=location)
        if status:
            jobs = jobs.filter(status=status)
        if sort_by:
            jobs = jobs.order_by(sort_by)
        else:
            jobs = jobs.order_by("-created_at")

    return render(request, "jobs/job_list.html", {"jobs": jobs, "form": form})


@login_required
def job_detail(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    return render(request, "jobs/job_detail.html", {"job": job})


@login_required
def create_job(request):
    if request.method == "POST":
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.poster = request.user
            job.save()

            Notification.objects.create(
                user=request.user,
                content=f"Your job '{job.title}' has been posted successfully",
                link=reverse("jobs:job_detail", kwargs={"job_id": job.id}),
                job=job,
            )
            return redirect("jobs:job_detail", job_id=job.id)
    else:
        form = JobForm()
    return render(request, "jobs/create_job.html", {"form": form})


@login_required
def apply_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    if job.status == "closed":
        messages.error(request, "This job is no longer accepting applications.")
        return redirect("jobs:job_detail", job_id=job.id)

    if request.method == "POST":
        form = ApplicationForm(request.POST, request.FILES, user=request.user, job=job)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.applicant = request.user
            application.save()

            # Create a conversation and send a message to job poster
            conversation, created = Conversation.objects.get_or_create(job=job)
            conversation.participants.add(request.user, job.poster)
            Message.objects.create(
                conversation=conversation,
                sender=request.user,
                content=f"New application received for {job.title}",
            )

            # Create a notification for the job poster
            Notification.objects.create(
                user=job.poster,
                content=f"New application received for {job.title}",
                link=reverse("jobs:view_applicants", kwargs={"job_id": job.id}),
                job=job,
            )

            messages.success(
                request, "Your application has been submitted successfully."
            )
            return redirect("jobs:job_detail", job_id=job.id)
    else:
        form = ApplicationForm(user=request.user, job=job)
    return render(request, "jobs/apply_job.html", {"form": form, "job": job})


@login_required
def update_application_status(request, application_id):
    application = get_object_or_404(
        Application, id=application_id, job__poster=request.user
    )
    if request.method == "POST":
        new_status = request.POST.get("status")
        if new_status in dict(Application.STATUS_CHOICES):
            application.status = new_status
            application.save()

            # Send a message to the applicant
            conversation, created = Conversation.objects.get_or_create(
                job=application.job
            )
            conversation.participants.add(request.user, application.applicant)
            Message.objects.create(
                conversation=conversation,
                sender=request.user,
                content=f"Your application for {application.job.title} has been {new_status}",
            )

            # Create a notification for the applicant
            Notification.objects.create(
                user=application.applicant,
                content=f"Your application for {application.job.title} has been {new_status}",
                link=reverse("jobs:job_detail", kwargs={"job_id": application.job.id}),
                job=application.job,
            )

            messages.success(request, f"Application status updated to {new_status}.")
        else:
            messages.error(request, "Invalid status.")
    return redirect("jobs:view_applicants", job_id=application.job.id)


@login_required
def update_job_status(request, job_id):
    job = get_object_or_404(Job, id=job_id, poster=request.user)
    if request.method == "POST":
        new_status = request.POST.get("status")
        if new_status in dict(Job.STATUS_CHOICES):
            old_status_display = job.get_status_display()
            job.status = new_status
            job.save()
            new_status_display = job.get_status_display()

            # Notify all applicants
            for application in job.applications.all():
                Notification.objects.create(
                    user=application.applicant,
                    content=f"The job '{job.title}' you applied for has been updated to {new_status_display}",
                    link=reverse("jobs:job_detail", kwargs={"job_id": job.id}),
                    job=job,
                )

            messages.success(
                request,
                f"Job status updated from {old_status_display} to {new_status_display}.",
            )
        else:
            messages.error(request, "Invalid status.")
    return redirect("jobs:job_detail", job_id=job.id)


@login_required
def view_applicants(request, job_id):
    job = get_object_or_404(Job, id=job_id, poster=request.user)
    applications = job.applications.all()
    return render(
        request, "jobs/view_applicants.html", {"job": job, "applications": applications}
    )


@login_required
def my_applications(request):
    applications = Application.objects.filter(applicant=request.user)
    return render(request, "jobs/my_applications.html", {"applications": applications})
