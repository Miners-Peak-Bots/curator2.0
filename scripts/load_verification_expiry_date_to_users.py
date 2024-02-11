from datetime import timedelta

from django.utils import timezone
from user.models import TeleUser

current_time = timezone.now()

for user in TeleUser.objects.filter(verified=True):
    latest_verified_log = user.vlogs.filter(event__in=[1, 3]).order_by('-created_at').first()
    expires_at = latest_verified_log.created_at + timedelta(days=365)

    user.verification_expires_at = expires_at
    user.save()
