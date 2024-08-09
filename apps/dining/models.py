from django.db import models
from django.conf import settings

class DiningHall(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    hours = models.TextField()
    
    def __str__(self):
        return self.name

class MenuItem(models.Model):
    dining_hall = models.ForeignKey(DiningHall, on_delete=models.CASCADE, related_name='menu_items')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    is_available = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.name} at {self.dining_hall.name}"

class DiningHallReview(models.Model):
    dining_hall = models.ForeignKey(DiningHall, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Review for {self.dining_hall.name} by {self.user.username}"