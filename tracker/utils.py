from django.utils import timezone
from datetime import timedelta
from django.db.models import Count, Avg, F

def calculate_streak(logs):
    """Calculate current and longest streak information"""
    if not logs.exists():
        return {
            'current_hours': 0,
            'current_days': 0,
            'longest_days': 0,
            'last_smoke': None
        }
    
    last_smoke = logs.first()
    current_streak = timezone.now() - last_smoke.timestamp
    current_hours = int(current_streak.total_seconds() / 3600)
    current_days = int(current_streak.days)
    
    # Calculate longest streak between smokes
    smoke_times = list(logs.values_list('timestamp', flat=True))
    longest_gap = timedelta(0)
    
    # Add current time to the list to calculate the ongoing streak as part of the longest
    smoke_times.insert(0, timezone.now())

    for i in range(len(smoke_times) - 1):
        gap = smoke_times[i] - smoke_times[i + 1]
        if gap > longest_gap:
            longest_gap = gap
    
    longest_days = longest_gap.days
    
    return {
        'current_hours': current_hours,
        'current_days': current_days,
        'longest_days': longest_days,
        'last_smoke': last_smoke
    }

def get_trigger_stats(logs):
    """Get trigger statistics with percentages"""
    total = logs.count()
    if total == 0:
        return []

    trigger_stats = logs.values('trigger').annotate(
        count=Count('trigger')
    ).order_by('-count')
    
    for stat in trigger_stats:
        stat['percentage'] = round((stat['count'] / total) * 100, 1)
        stat['trigger_display'] = dict(logs.model.TRIGGER_CHOICES).get(stat['trigger'])
    
    return trigger_stats

def get_mood_impact(logs):
    """Calculate mood impact statistics"""
    mood_data = logs.exclude(mood_before__isnull=True, mood_after__isnull=True)
    
    if not mood_data.exists():
        return None
    
    avg_before = mood_data.aggregate(avg=Avg('mood_before'))['avg']
    avg_after = mood_data.aggregate(avg=Avg('mood_after'))['avg']
    
    improved = mood_data.filter(mood_after__gt=F('mood_before')).count()
    worsened = mood_data.filter(mood_after__lt=F('mood_before')).count()
    unchanged = mood_data.filter(mood_after=F('mood_before')).count()
    
    total = mood_data.count()
    
    return {
        'avg_before': round(avg_before, 1) if avg_before else 0,
        'avg_after': round(avg_after, 1) if avg_after else 0,
        'improved_percent': round((improved / total) * 100, 1) if total > 0 else 0,
        'worsened_percent': round((worsened / total) * 100, 1) if total > 0 else 0,
        'unchanged_percent': round((unchanged / total) * 100, 1) if total > 0 else 0,
    }
