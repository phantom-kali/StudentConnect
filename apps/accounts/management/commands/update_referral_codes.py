from django.core.management.base import BaseCommand
from apps.accounts.models import User

class Command(BaseCommand):
    help = 'Updates null referral codes with new unique codes'

    def handle(self, *args, **options):
        users_without_codes = User.objects.filter(referral_code__isnull=True)
        for user in users_without_codes:
            user.save()  # This will trigger the save method and generate a new code
        self.stdout.write(self.style.SUCCESS(f'Successfully updated {users_without_codes.count()} users'))