from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import SmokeLog, Brand
from .forms import SmokeLogForm, BrandForm
from django.db.models import Count, Sum
from django.db.models.functions import TruncDate, TruncWeek, TruncHour
import json
from datetime import datetime, timedelta
from django.utils import timezone

@login_required
def home(request):
    return render(request, 'tracker/home.html')

@login_required
def log_smoke(request):
    if request.method == 'POST':
        form = SmokeLogForm(request.POST)
        if form.is_valid():
            log = form.save(commit=False)
            log.user = request.user
            log.save()
            return redirect('log_list')
    else:
        form = SmokeLogForm()
    return render(request, 'tracker/log_smoke.html', {'form': form})

@login_required
def log_list(request):
    logs = SmokeLog.objects.filter(user=request.user).order_by('-timestamp')
    return render(request, 'tracker/log_list.html', {'logs': logs})

@login_required
def add_brand(request):
    if request.method == 'POST':
        form = BrandForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('brand_list')
    else:
        form = BrandForm()
    return render(request, 'tracker/add_brand.html', {'form': form})

@login_required
def brand_list(request):
    brands = Brand.objects.all()
    return render(request, 'tracker/brand_list.html', {'brands': brands})

@login_required
def stats(request):
    user = request.user
    now = timezone.now()
    
    # General stats
    all_logs = SmokeLog.objects.filter(user=user)
    total_smokes = all_logs.count()
    last_smoke = all_logs.order_by('-timestamp').first()
    total_cost = all_logs.aggregate(total_cost=Sum('brand__price'))['total_cost'] or 0

    # Daily chart (count vs hour for all 24 hours)
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    today_logs = all_logs.filter(timestamp__gte=today_start)
    daily_data = today_logs.annotate(hour=TruncHour('timestamp')).values('hour').annotate(count=Count('id')).order_by('hour')
    daily_counts_dict = {d['hour'].hour: d['count'] for d in daily_data}
    daily_labels = [f"{h:02d}:00" for h in range(24)]
    daily_counts = [daily_counts_dict.get(h, 0) for h in range(24)]

    # Weekly chart (count vs day for all 7 days)
    week_start = today_start - timedelta(days=now.weekday())
    week_logs = all_logs.filter(timestamp__gte=week_start, timestamp__lt=week_start + timedelta(days=7))
    weekly_data = week_logs.annotate(date=TruncDate('timestamp')).values('date').annotate(count=Count('id')).order_by('date')
    week_counts_dict = {d['date'].weekday(): d['count'] for d in weekly_data}
    weekly_labels = [(week_start + timedelta(days=i)).strftime('%A') for i in range(7)]
    weekly_counts = [week_counts_dict.get(i, 0) for i in range(7)]

    # Monthly chart (count vs week for all weeks in the month)
    month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    month_logs = all_logs.filter(timestamp__gte=month_start)
    monthly_data = month_logs.annotate(week=TruncWeek('timestamp')).values('week').annotate(count=Count('id')).order_by('week')
    
    # Create labels for every week of the current month
    first_day_of_month = month_start
    first_week_of_month = first_day_of_month - timedelta(days=first_day_of_month.weekday())
    
    monthly_labels = []
    current_week = first_week_of_month
    while current_week.month == now.month or (current_week.month == now.month-1 and current_week.day > 20):
        monthly_labels.append(f"Week of {current_week.strftime('%b %d')}")
        current_week += timedelta(weeks=1)
        if current_week.year > now.year: break

    month_counts_dict = {d['week'].strftime('%Y-%m-%d'): d['count'] for d in monthly_data}
    monthly_counts = []
    current_week_for_data = first_week_of_month
    for _ in monthly_labels:
        week_str = current_week_for_data.strftime('%Y-%m-%d')
        monthly_counts.append(month_counts_dict.get(week_str, 0))
        current_week_for_data += timedelta(weeks=1)

    context = {
        'total_smokes': total_smokes,
        'last_smoke': last_smoke,
        'total_cost': total_cost,
        'daily_labels': json.dumps(daily_labels),
        'daily_counts': json.dumps(daily_counts),
        'weekly_labels': json.dumps(weekly_labels),
        'weekly_counts': json.dumps(weekly_counts),
        'monthly_labels': json.dumps(monthly_labels),
        'monthly_counts': json.dumps(monthly_counts),
    }
    return render(request, 'tracker/stats.html', context)

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})
