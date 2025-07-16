from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import SmokeLog, UserPoints, Achievement, UserAchievement
from .achievement_service import check_and_award_achievements

@receiver(post_save, sender=SmokeLog)
def award_points_for_log(sender, instance, created, **kwargs):
    if created:
        # Award points for logging
        points_to_award = 10
        user_points, _ = UserPoints.objects.get_or_create(user=instance.user)
        user_points.points += points_to_award
        user_points.save()

        # Check for achievements
        check_and_award_achievements(instance.user)
