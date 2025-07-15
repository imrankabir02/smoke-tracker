from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import SmokeLog, UserPoints, Achievement, UserAchievement

@receiver(post_save, sender=SmokeLog)
def award_points_for_log(sender, instance, created, **kwargs):
    if created:
        # Award points for logging
        points_to_award = 10  # Example: 10 points per log
        user_points, _ = UserPoints.objects.get_or_create(user=instance.user)
        user_points.points += points_to_award
        user_points.save()

        # Check for "First Log" achievement
        try:
            first_log_achievement = Achievement.objects.get(title="First Log")
            if not UserAchievement.objects.filter(user=instance.user, achievement=first_log_achievement).exists():
                UserAchievement.objects.create(user=instance.user, achievement=first_log_achievement)
                user_points.points += first_log_achievement.points_reward
                user_points.save()
        except Achievement.DoesNotExist:
            # Handle case where achievement is not yet created
            pass
