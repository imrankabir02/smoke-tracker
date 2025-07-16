from celery import shared_task
from django.contrib.auth.models import User
from .achievement_service import check_and_award_achievements

@shared_task
def check_all_user_achievements():
    """
    Periodically check achievements for all users.
    This is useful for time-based achievements like streaks.
    """
    users = User.objects.all()
    for user in users:
        check_achievements_for_user.delay(user.id)

@shared_task
def check_achievements_for_user(user_id):
    """
    Check and award achievements for a single user.
    """
    try:
        user = User.objects.get(id=user_id)
        check_and_award_achievements(user)
    except User.DoesNotExist:
        return
