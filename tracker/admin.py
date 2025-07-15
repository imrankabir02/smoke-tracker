from django.contrib import admin
from .models import (
    Brand, UserBrand, DailyGoal, SmokeLog, UserDefault, Profile,
    UserPoints, Achievement, UserAchievement
)

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)

@admin.register(UserBrand)
class UserBrandAdmin(admin.ModelAdmin):
    list_display = ('user', 'brand', 'price')
    list_filter = ('user',)
    search_fields = ('user__username', 'brand__name')

@admin.register(DailyGoal)
class DailyGoalAdmin(admin.ModelAdmin):
    list_display = ('user', 'daily_limit', 'updated_at')
    search_fields = ('user__username',)

@admin.register(SmokeLog)
class SmokeLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_brand', 'timestamp', 'trigger', 'mood_before', 'mood_after')
    list_filter = ('user', 'trigger', 'timestamp')
    search_fields = ('user__username', 'user_brand__brand__name', 'note')
    date_hierarchy = 'timestamp'

@admin.register(UserDefault)
class UserDefaultAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_brand', 'trigger')
    list_filter = ('user',)
    search_fields = ('user__username', 'user_brand__brand__name')

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'timezone', 'currency', 'setup_complete')
    search_fields = ('user__username',)
    list_filter = ('setup_complete',)
    list_editable = ('timezone', 'currency', 'setup_complete')

@admin.register(UserPoints)
class UserPointsAdmin(admin.ModelAdmin):
    list_display = ('user', 'points', 'last_updated')
    search_fields = ('user__username',)

@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ('title', 'points_reward')
    search_fields = ('title',)

@admin.register(UserAchievement)
class UserAchievementAdmin(admin.ModelAdmin):
    list_display = ('user', 'achievement', 'date_earned')
    list_filter = ('user', 'achievement')
    search_fields = ('user__username', 'achievement__title')
