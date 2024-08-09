from django.contrib.auth.models import AbstractUser
from django.db import IntegrityError
from django.utils import timezone
from django.db import models
import uuid


class User(AbstractUser):
    email = models.EmailField(unique=True)
    is_student = models.BooleanField(default=True)
    bio = models.CharField(max_length=1000)
    location = models.CharField(max_length=100, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(
        upload_to="profile_pics/", null=True, blank=True
    )

    followers = models.ManyToManyField(
        "self", symmetrical=False, related_name="following"
    )

    is_premium = models.BooleanField(default=False)
    premium_until = models.DateTimeField(null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    referral_code = models.CharField(max_length=20, unique=True, blank=True, null=True)
    referred_by = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="referrals",
    )
    referral_count = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.referral_code:
            while True:
                generated_code = self.generate_referral_code()
                if not User.objects.filter(referral_code=generated_code).exists():
                    self.referral_code = generated_code
                    break
        super().save(*args, **kwargs)

    def generate_referral_code(self):
        return f"{self.username[:5]}{uuid.uuid4().hex[:10]}"

    def add_referral(self, referred_user):
        self.referral_count += 1
        if self.referral_count % 5 == 0:  # Every 5 referrals
            self.is_premium = True
            self.premium_until = timezone.now() + timezone.timedelta(days=7)
        self.save()
        referred_user.referred_by = self
        referred_user.save()

    def __str__(self):
        return self.email
