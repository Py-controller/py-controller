from datetime import timedelta
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.db.models import F


def delete_inactive_users():
    User = get_user_model()
    time_to_inactive = timedelta(minutes=30)
    print("teste")
    now = timezone.now()
    inactive_users = User.objects.filter(
        is_active=True, last_login__lte=now - time_to_inactive
    )

    inactive_users.update(is_active=False)
