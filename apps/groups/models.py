from django.db import models
from django.conf import settings

class Group(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='custom_groups')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class GroupPost(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='posts')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} in {self.group.name}: {self.content[:50]}"