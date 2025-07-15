from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
import pytz

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    timezone = models.CharField(max_length=50, default='UTC', choices=[(tz, tz) for tz in pytz.all_timezones])
    currency = models.CharField(max_length=10, default='USD')
    setup_complete = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}'s Profile"


class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class UserBrand(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ('user', 'brand')
        ordering = ['brand__name']

    def __str__(self):
        return f"{self.user.username}'s {self.brand.name} - {self.user.profile.currency}{self.price}"

class DailyGoal(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    daily_limit = models.IntegerField(default=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.daily_limit}/day"

class SmokeLog(models.Model):
    TRIGGER_CHOICES = [
        ('stress', 'Stress'),
        ('boredom', 'Boredom'),
        ('social', 'Social'),
        ('habit', 'Habit/Routine'),
        ('craving', 'Craving'),
        ('after_meal', 'After Meal'),
        ('break', 'Work Break'),
        ('alcohol', 'With Alcohol'),
        ('other', 'Other'),
    ]
    
    MOOD_CHOICES = [
        (1, '😫 Very Bad'),
        (2, '😞 Bad'),
        (3, '😐 Neutral'),
        (4, '😊 Good'),
        (5, '😄 Very Good'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_brand = models.ForeignKey(UserBrand, on_delete=models.SET_NULL, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    trigger = models.CharField(max_length=20, choices=TRIGGER_CHOICES, default='other')
    mood_before = models.IntegerField(choices=MOOD_CHOICES, default=3)
    mood_after = models.IntegerField(choices=MOOD_CHOICES, default=3)
    note = models.TextField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.timestamp.strftime('%Y-%m-%d %H:%M')}"

    @property
    def mood_difference(self):
        return self.mood_after - self.mood_before

    class Meta:
        ordering = ['-timestamp']

class UserDefault(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_brand = models.ForeignKey(UserBrand, on_delete=models.SET_NULL, null=True, blank=True)
    trigger = models.CharField(max_length=20, choices=SmokeLog.TRIGGER_CHOICES, default='other')
    mood_before = models.IntegerField(choices=SmokeLog.MOOD_CHOICES, default=3)
    mood_after = models.IntegerField(choices=SmokeLog.MOOD_CHOICES, default=3)

    def __str__(self):
        return f"Defaults for {self.user.username}"


class BrandRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    brand_name = models.CharField(max_length=100)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Request for '{self.brand_name}' by {self.user.username} ({self.status})"

    class Meta:
        ordering = ['-created_at']
        unique_together = ('user', 'brand_name')


class UserPoints(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.points} Points"

class Achievement(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    points_reward = models.IntegerField(default=0)
    icon = models.ImageField(upload_to='achievement_icons/', blank=True, null=True)
    
    def __str__(self):
        return self.title

class UserAchievement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    date_earned = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'achievement')

    def __str__(self):
        return f"{self.user.username} earned {self.achievement.title}"
