# Generated by Django 4.2.11 on 2024-08-05 21:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0002_application_status_job_status'),
        ('messaging', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='conversation',
            name='job',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='conversations', to='jobs.job'),
        ),
    ]
