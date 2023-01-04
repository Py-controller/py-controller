from datetime import timedelta
from django.utils import timezone
from django.contrib.auth import get_user_model


def delete_inactive_users():
    User = get_user_model()
    time_to_inactive = timedelta(days=180)
    now = timezone.now()
    inactive_users = User.objects.filter(
        is_active=False, last_login__lte=now - time_to_inactive
    )
    inactive_users.delete()
