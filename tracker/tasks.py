from celery import shared_task
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from .models import SmokeLog, Achievement, UserAchievement, UserPoints

@shared_task
def check_all_user_streaks():
    users = User.objects.all()
    for user in users:
        check_streak_for_user.delay(user.id)

@shared_task
def check_streak_for_user(user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return

    today = timezone.now().date()
    yesterday = today - timedelta(days=1)

    # Check if the user smoked yesterday
    smoked_yesterday = SmokeLog.objects.filter(user=user, timestamp__date=yesterday).exists()

    if smoked_yesterday:
        # If they smoked yesterday, their streak is 0
        # (No action needed unless you want to store the streak count)
        return

    # If they didn't smoke yesterday, check their last smoke
    last_smoke = SmokeLog.objects.filter(user=user).order_by('-timestamp').first()
    
    if not last_smoke:
        # No smokes ever, this logic might need refinement based on product decision
        return

    days_since_last_smoke = (today - last_smoke.timestamp.date()).days

    # Define streak achievements
    streak_achievements = {
        1: "First Smoke-Free Day",
        7: "7-Day Streak",
        30: "30-Day Streak",
    }

    for days, achievement_title in streak_achievements.items():
        if days_since_last_smoke >= days:
            try:
                achievement = Achievement.objects.get(title=achievement_title)
                if not UserAchievement.objects.filter(user=user, achievement=achievement).exists():
                    UserAchievement.objects.create(user=user, achievement=achievement)
                    user_points, _ = UserPoints.objects.get_or_create(user=user)
                    user_points.points += achievement.points_reward
                    user_points.save()
            except Achievement.DoesNotExist:
                continue
