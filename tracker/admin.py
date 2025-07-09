from django.contrib import admin
from .models import Brand, UserBrand, DailyGoal, SmokeLog, UserDefault

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
