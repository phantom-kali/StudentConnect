from django.db import models
from django.conf import settings


class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="liked_posts", blank=True
    )
    view_count = models.PositiveIntegerField(default=0)
    tags = models.ManyToManyField("Tag", related_name="posts", blank=True)
    media = models.FileField(upload_to="post_media/", null=True, blank=True)

    view_count = models.PositiveIntegerField(default=0)

    def increment_view_count(self):
        self.view_count += 1
        self.save()

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username}: {self.content[:50]}"


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    content = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} on {self.post}: {self.content[:30]}"


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)


class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class ReportOption(models.Model):
    reason = models.CharField(max_length=100)

    def __str__(self):
        return self.reason

class Report(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    reason = models.ForeignKey(ReportOption, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
