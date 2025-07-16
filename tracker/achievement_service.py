from .models import SmokeLog, Achievement, UserAchievement, UserPoints
from django.utils import timezone
from datetime import timedelta

def get_user_progress(user, achievement):
    """
    Calculate the user's progress towards a specific achievement.
    """
    if achievement.criteria_type == 'total_logs':
        current_value = SmokeLog.objects.filter(user=user).count()
        goal_value = achievement.criteria_value
        progress = (current_value / goal_value) * 100
        return {
            'current': current_value,
            'goal': goal_value,
            'progress': min(progress, 100)
        }
    elif achievement.criteria_type == 'streak_days':
        last_smoke = SmokeLog.objects.filter(user=user).order_by('-timestamp').first()
        if not last_smoke:
            # If user has no logs, they have a perfect streak
            current_value = achievement.criteria_value 
        else:
            current_value = (timezone.now() - last_smoke.timestamp).days
        
        goal_value = achievement.criteria_value
        progress = (current_value / goal_value) * 100 if goal_value > 0 else 100
        return {
            'current': current_value,
            'goal': goal_value,
            'progress': min(progress, 100)
        }
    return None

def check_and_award_achievements(user):
    """
    Check all achievements for a user and award them if the criteria are met.
    """
    unlocked_achievements = UserAchievement.objects.filter(user=user).values_list('achievement_id', flat=True)
    achievements_to_check = Achievement.objects.exclude(id__in=unlocked_achievements)

    for achievement in achievements_to_check:
        progress_data = get_user_progress(user, achievement)
        if progress_data and progress_data['current'] >= progress_data['goal']:
            UserAchievement.objects.create(user=user, achievement=achievement)
            user_points, _ = UserPoints.objects.get_or_create(user=user)
            user_points.points += achievement.points_reward
            user_points.save()
