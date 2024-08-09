from django.core.management.base import BaseCommand
from django.utils import timezone
from django.urls import reverse
from jobs.models import Job
from notifications.models import Notification

class Command(BaseCommand):
    help = 'Send notifications for jobs with approaching deadlines'

    def handle(self, *args, **options):
        today = timezone.now().date()
        upcoming_jobs = Job.objects.filter(
            status='open',
            deadline__gt=today,
            deadline__lte=today + timezone.timedelta(days=3)
        )

        for job in upcoming_jobs:
            Notification.objects.create(
                user=job.poster,
                content=f"Your job '{job.title}' is closing in {(job.deadline - today).days} days",
                link=reverse('jobs:job_detail', kwargs={'job_id': job.id}),
                job=job
            )

        self.stdout.write(self.style.SUCCESS(f'Sent notifications for {upcoming_jobs.count()} jobs'))