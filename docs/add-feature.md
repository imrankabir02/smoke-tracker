# 🚬 Complete Smoking Tracker Development Plan

## ✅ Project Overview

**Goal**: Help users log smoking events, track triggers and mood patterns, set daily goals, and monitor streaks to effectively reduce or quit smoking.

**Target Users**: Smokers who want to quit or reduce smoking through data-driven insights and behavioral tracking.

---

## 📌 Phase 1: Requirements & Planning

### 🎯 Core Features:

1. **Authentication System**
   - User Registration & Login
   - Secure user sessions
   - Password reset functionality

2. **Smoking Log Management**
   - Log smoking events with timestamp
   - Select cigarette brand and price
   - Track triggers (stress, boredom, social, etc.)
   - Rate mood before and after smoking
   - Add optional notes

3. **Goal Setting & Progress Tracking**
   - Set daily smoking limits
   - Visual progress bars
   - Streak counter (hours since last smoke)
   - Daily/weekly comparisons

4. **Analytics & Insights**
   - Total smokes and costs
   - Trigger pattern analysis
   - Mood impact assessment
   - Streak statistics
   - Weekly progress reports

5. **Dashboard & Navigation**
   - Clean, intuitive interface
   - Quick access to key metrics
   - Mobile-responsive design

### 📦 Tech Stack:

| Layer          | Tool                                             |
| -------------- | ------------------------------------------------ |
| Backend        | Django 4.2+                                      |
| Frontend       | Django Templates + Bootstrap 5                   |
| Database       | SQLite (dev), PostgreSQL (production)           |
| Authentication | Django built-in auth system                      |
| Deployment     | PythonAnywhere / Heroku / Render                 |
| Charts         | Chart.js for data visualization                  |
| Icons          | Bootstrap Icons                                  |

---

## 🏗️ Phase 2: Project Structure

```bash
smoketracker/
├── smoketracker/                    # Project settings
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── tracker/                         # Main app
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   ├── utils.py                     # Helper functions
│   ├── migrations/
│   ├── templates/
│   │   └── tracker/
│   │       ├── base.html
│   │       ├── home.html
│   │       ├── log_smoke.html
│   │       ├── log_list.html
│   │       ├── stats.html
│   │       ├── brands.html
│   │       ├── add_brand.html
│   │       └── set_goal.html
│   └── templatetags/
│       └── tracker_extras.py        # Custom template filters
├── templates/                       # Global templates
│   └── registration/
│       ├── login.html
│       ├── signup.html
│       └── password_reset.html
├── static/                          # Static files
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── app.js
│   └── images/
├── requirements.txt
├── .env.example
├── .gitignore
├── db.sqlite3
└── manage.py
```

---

## ⚙️ Phase 3: Implementation Plan

### 3.1 Project Setup

**Commands:**
```bash
# Create project
django-admin startproject smoketracker
cd smoketracker

# Create app
python manage.py startapp tracker

# Install dependencies
pip install django python-decouple psycopg2-binary
pip freeze > requirements.txt

# Initial migration
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

**Settings Configuration:**
```python
# settings.py
import os
from decouple import config

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tracker',
]

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Static files
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Login/Logout redirects
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'

# Time zone
TIME_ZONE = 'UTC'
USE_TZ = True
```

---

### 3.2 Authentication System

**URLs Configuration:**
```python
# smoketracker/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('tracker.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
]
```

**Custom Signup View:**
```python
# tracker/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

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
```

---

### 3.3 Models

```python
# tracker/models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - ${self.price}"

    class Meta:
        ordering = ['name']

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
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True)
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
```

---

### 3.4 Forms

```python
# tracker/forms.py
from django import forms
from .models import Brand, SmokeLog, DailyGoal

class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ['name', 'price']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Marlboro Red'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'placeholder': 'e.g., 12.50'
            }),
        }

class SmokeLogForm(forms.ModelForm):
    class Meta:
        model = SmokeLog
        fields = ['brand', 'trigger', 'mood_before', 'mood_after', 'note']
        widgets = {
            'brand': forms.Select(attrs={'class': 'form-select'}),
            'trigger': forms.Select(attrs={'class': 'form-select'}),
            'mood_before': forms.Select(attrs={'class': 'form-select'}),
            'mood_after': forms.Select(attrs={'class': 'form-select'}),
            'note': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Optional notes about this smoke...'
            }),
        }

class DailyGoalForm(forms.ModelForm):
    class Meta:
        model = DailyGoal
        fields = ['daily_limit']
        widgets = {
            'daily_limit': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'max': '50',
                'placeholder': 'e.g., 10'
            }),
        }
        labels = {
            'daily_limit': 'Daily Smoking Limit'
        }
```

---

### 3.5 Views & Logic

```python
# tracker/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from django.utils import timezone
from django.db.models import Count, Sum, Avg
from datetime import datetime, timedelta
from .models import SmokeLog, Brand, DailyGoal
from .forms import SmokeLogForm, BrandForm, DailyGoalForm
from .utils import calculate_streak, get_trigger_stats, get_mood_impact

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Welcome! Your account has been created.')
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def home(request):
    logs = SmokeLog.objects.filter(user=request.user)
    last_smoke = logs.first()
    
    # Calculate streak
    if last_smoke:
        time_since_last = timezone.now() - last_smoke.timestamp
        hours_since_last = int(time_since_last.total_seconds() / 3600)
        minutes_since_last = int((time_since_last.total_seconds() % 3600) / 60)
    else:
        hours_since_last = 0
        minutes_since_last = 0
    
    # Daily progress
    today = timezone.now().date()
    today_smokes = logs.filter(timestamp__date=today).count()
    
    try:
        daily_goal = DailyGoal.objects.get(user=request.user)
        daily_limit = daily_goal.daily_limit
    except DailyGoal.DoesNotExist:
        daily_limit = 10
    
    progress_percentage = min(100, (today_smokes / daily_limit) * 100) if daily_limit > 0 else 0
    
    # Recent activity
    recent_logs = logs[:5]
    
    context = {
        'hours_since_last': hours_since_last,
        'minutes_since_last': minutes_since_last,
        'today_smokes': today_smokes,
        'daily_limit': daily_limit,
        'progress_percentage': progress_percentage,
        'recent_logs': recent_logs,
        'last_smoke': last_smoke,
    }
    
    return render(request, 'tracker/home.html', context)

@login_required
def log_smoke(request):
    if request.method == 'POST':
        form = SmokeLogForm(request.POST)
        if form.is_valid():
            smoke_log = form.save(commit=False)
            smoke_log.user = request.user
            smoke_log.save()
            messages.success(request, 'Smoke logged successfully!')
            return redirect('home')
    else:
        form = SmokeLogForm()
    
    return render(request, 'tracker/log_smoke.html', {'form': form})

@login_required
def log_list(request):
    logs = SmokeLog.objects.filter(user=request.user)
    
    # Filter by trigger
    trigger_filter = request.GET.get('trigger')
    if trigger_filter:
        logs = logs.filter(trigger=trigger_filter)
    
    # Filter by date range
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    if date_from:
        logs = logs.filter(timestamp__date__gte=date_from)
    if date_to:
        logs = logs.filter(timestamp__date__lte=date_to)
    
    # Pagination
    from django.core.paginator import Paginator
    paginator = Paginator(logs, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'trigger_choices': SmokeLog.TRIGGER_CHOICES,
        'trigger_filter': trigger_filter,
        'date_from': date_from,
        'date_to': date_to,
    }
    
    return render(request, 'tracker/log_list.html', context)

@login_required
def stats(request):
    logs = SmokeLog.objects.filter(user=request.user)
    total_smokes = logs.count()
    
    if total_smokes == 0:
        return render(request, 'tracker/stats.html', {'no_data': True})
    
    last_smoke = logs.first()
    total_cost = logs.aggregate(total_cost=Sum('brand__price'))['total_cost'] or 0
    
    # Time-based stats
    today = timezone.now().date()
    week_ago = today - timedelta(days=7)
    month_ago = today - timedelta(days=30)
    
    today_smokes = logs.filter(timestamp__date=today).count()
    this_week = logs.filter(timestamp__date__gte=week_ago).count()
    this_month = logs.filter(timestamp__date__gte=month_ago).count()
    
    last_week = logs.filter(
        timestamp__date__gte=week_ago - timedelta(days=7),
        timestamp__date__lt=week_ago
    ).count()
    
    # Advanced analytics
    trigger_stats = get_trigger_stats(logs)
    mood_impact = get_mood_impact(logs)
    streak_info = calculate_streak(logs)
    
    # Daily average
    if logs.exists():
        first_log = logs.last()
        days_tracking = (timezone.now().date() - first_log.timestamp.date()).days + 1
        daily_average = round(total_smokes / days_tracking, 1)
    else:
        daily_average = 0
    
    context = {
        'total_smokes': total_smokes,
        'total_cost': total_cost,
        'last_smoke': last_smoke,
        'today_smokes': today_smokes,
        'this_week': this_week,
        'this_month': this_month,
        'last_week': last_week,
        'daily_average': daily_average,
        'trigger_stats': trigger_stats,
        'mood_impact': mood_impact,
        'streak_info': streak_info,
    }
    
    return render(request, 'tracker/stats.html', context)

@login_required
def brands(request):
    brands = Brand.objects.all()
    return render(request, 'tracker/brands.html', {'brands': brands})

@login_required
def add_brand(request):
    if request.method == 'POST':
        form = BrandForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Brand added successfully!')
            return redirect('brands')
    else:
        form = BrandForm()
    
    return render(request, 'tracker/add_brand.html', {'form': form})

@login_required
def set_goal(request):
    try:
        goal = DailyGoal.objects.get(user=request.user)
    except DailyGoal.DoesNotExist:
        goal = None
    
    if request.method == 'POST':
        form = DailyGoalForm(request.POST, instance=goal)
        if form.is_valid():
            goal = form.save(commit=False)
            goal.user = request.user
            goal.save()
            messages.success(request, 'Daily goal updated successfully!')
            return redirect('home')
    else:
        form = DailyGoalForm(instance=goal)
    
    return render(request, 'tracker/set_goal.html', {'form': form, 'goal': goal})
```

---

### 3.6 Helper Functions

```python
# tracker/utils.py
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count, Avg

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
    
    for i in range(len(smoke_times) - 1):
        gap = smoke_times[i] - smoke_times[i + 1]
        if gap > longest_gap:
            longest_gap = gap
    
    longest_days = longest_gap.days
    
    return {
        'current_hours': current_hours,
        'current_days': current_days,
        'longest_days': max(longest_days, current_days),
        'last_smoke': last_smoke
    }

def get_trigger_stats(logs):
    """Get trigger statistics with percentages"""
    trigger_stats = logs.values('trigger').annotate(
        count=Count('trigger')
    ).order_by('-count')
    
    total = logs.count()
    
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
    
    improved = mood_data.filter(mood_after__gt=mood_before).count()
    worsened = mood_data.filter(mood_after__lt=mood_before).count()
    unchanged = mood_data.filter(mood_after=mood_before).count()
    
    total = mood_data.count()
    
    return {
        'avg_before': round(avg_before, 1) if avg_before else 0,
        'avg_after': round(avg_after, 1) if avg_after else 0,
        'improved_percent': round((improved / total) * 100, 1) if total > 0 else 0,
        'worsened_percent': round((worsened / total) * 100, 1) if total > 0 else 0,
        'unchanged_percent': round((unchanged / total) * 100, 1) if total > 0 else 0,
    }
```

---

### 3.7 URL Configuration

```python
# tracker/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('log/', views.log_smoke, name='log_smoke'),
    path('logs/', views.log_list, name='log_list'),
    path('stats/', views.stats, name='stats'),
    path('brands/', views.brands, name='brands'),
    path('add-brand/', views.add_brand, name='add_brand'),
    path('set-goal/', views.set_goal, name='set_goal'),
    path('signup/', views.signup, name='signup'),
]
```

---

### 3.8 Templates

#### Base Template
```html
<!-- tracker/templates/tracker/base.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Smoke Tracker{% endblock %}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.8.1/font/bootstrap-icons.css" rel="stylesheet">
    <style>
        .streak-counter {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 15px;
            padding: 20px;
            text-align: center;
            margin-bottom: 20px;
        }
        .progress-card {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
            border-radius: 15px;
            padding: 20px;
        }
        .stats-card {
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            color: white;
            border-radius: 15px;
            padding: 20px;
        }
    </style>
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container">
            <a class="navbar-brand" href="{% url 'home' %}">
                <i class="bi bi-activity"></i> Smoke Tracker
            </a>
            
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav me-auto">
                    {% if user.is_authenticated %}
                        <li class="nav-item">
                            <a class="nav-link" href="{% url 'home' %}">Dashboard</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="{% url 'log_smoke' %}">Log Smoke</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="{% url 'logs' %}">View Logs</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="{% url 'stats' %}">Statistics</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="{% url 'brands' %}">Brands</a>
                        </li>
                    {% endif %}
                </ul>
                
                <ul class="navbar-nav">
                    {% if user.is_authenticated %}
                        <li class="nav-item dropdown">
                            <a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-bs-toggle="dropdown">
                                <i class="bi bi-person-circle"></i> {{ user.username }}
                            </a>
                            <ul class="dropdown-menu">
                                <li><a class="dropdown-item" href="{% url 'set_goal' %}">Set Daily Goal</a></li>
                                <li><hr class="dropdown-divider"></li>
                                <li><a class="dropdown-item" href="{% url 'logout' %}">Logout</a></li>
                            </ul>
                        </li>
                    {% else %}
                        <li class="nav-item">
                            <a class="nav-link" href="{% url 'login' %}">Login</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="{% url 'signup' %}">Sign Up</a>
                        </li>
                    {% endif %}
                </ul>
            </div>
        </div>
    </nav>

    <div class="container mt-4">
        {% if messages %}
            {% for message in messages %}
                <div class="alert alert-{{ message.tags }} alert-dismissible fade show" role="alert">
                    {{ message }}
                    <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                </div>
            {% endfor %}
        {% endif %}

        {% block content %}
        {% endblock %}
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    {% block scripts %}
    {% endblock %}
</body>
</html>
```

#### Home Dashboard
```html
<!-- tracker/templates/tracker/home.html -->
{% extends 'tracker/base.html' %}

{% block title %}Dashboard - Smoke Tracker{% endblock %}

{% block content %}
<div class="row">
    <div class="col-md-8">
        <div class="streak-counter">
            <h3><i class="bi bi-trophy"></i> Current Streak</h3>
            <h1>{{ hours_since_last }} hours, {{ minutes_since_last }} minutes</h1>
            <p class="mb-0">since your last smoke</p>
        </div>
        
        <div class="progress-card">
            <h4><i class="bi bi-target"></i> Daily Progress</h4>
            <h2>{{ today_smokes }} / {{ daily_limit }}</h2>
            <div class="progress mb-2" style="height: 10px;">
                <div class="progress-bar" role="progressbar" style="width: {{ progress_percentage }}%"></div>
            </div>
            <small>
                {% if today_smokes < daily_limit %}
                    {{ daily_limit|add:"-"|add:today_smokes }} remaining today
                {% else %}
                    Daily limit reached
                {% endif %}
            </small>
        </div>
    </div>
    
    <div class="col-md-4">
        <div class="card">
            <div class="card-body">
                <h5 class="card-title">Quick Actions</h5>
                <a href="{% url 'log_smoke' %}" class="btn btn-primary w-100 mb-2">
                    <i class="bi bi-plus-circle"></i> Log Smoke
                </a>
                <a href="{% url 'stats' %}" class="btn btn-info w-100 mb-2">
                    <i class="bi bi-graph-up"></i> View Stats
                </a>
                <a href="{% url 'set_goal' %}" class="btn btn-secondary w-100">
                    <i class="bi bi-gear"></i> Set Goal
                </a>
            </div>
        </div>
    </div>
</div>

{% if recent_logs %}
<div class="row mt-4">
    <div class="col-12">
        <h3>Recent Activity</h3>
        <div class="table-responsive">
            <table class="table table-striped">
                <thead>
                    <tr>
                        <th>Time</th>
                        <th>Brand</th>
                        <th>Trigger</th>
                        <th>Mood Change</th>
                    </tr>
                </thead>
                <tbody>
                    {% for log in recent_logs %}
                    <tr>
                        <td>{{ log.timestamp|date:"M d, H:i" }}</td>
                        <td>{{ log.brand|default:"Unknown" }}</td>
                        <td>{{ log.get_trigger_display }}</td>
                        <td>
                            {% if log.mood_difference > 0 %}
                                <span class="text-success">+{{ log.mood_difference }}</span>
                            {% elif log.mood_difference < 0 %}
                                <span class="text-danger">{{ log.mood_difference }}</span>
                            {% else %}
                                <span class="text-muted">0</span>
                            {% endif %}
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
        <a href="{% url 'log_list' %}" class="btn btn-outline-primary">View All Logs</a>
    </div>
</div>
{% endif %}
{% endblock %}
```

#### Log Smoke Form
```html
<!-- tracker/templates/tracker/log_smoke.html -->
{% extends 'tracker/base