from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils import timezone
from django.db.models import Count, Sum, Avg
from datetime import datetime, timedelta
from .models import SmokeLog, Brand, DailyGoal, UserDefault, UserBrand, Profile, BrandRequest
from .forms import SmokeLogForm, BrandForm, DailyGoalForm, UserDefaultForm, UserBrandForm, ProfileForm, SignUpForm, BrandRequestForm
from .utils import calculate_streak, get_trigger_stats, get_mood_impact

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            profile = Profile.objects.create(
                user=user,
                timezone=form.cleaned_data['timezone'],
                currency=form.cleaned_data['currency']
            )
            profile.save()
            login(request, user)
            messages.success(request, 'Welcome! Your account has been created.')
            return redirect('setup_start')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def home(request):
    timezone.activate(request.user.profile.timezone)
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
        daily_limit = 10 # Default value
    
    progress_percentage = min(100, (today_smokes / daily_limit) * 100) if daily_limit > 0 else 0
    
    # Recent activity
    recent_logs = logs[:1]

    try:
        user_defaults = UserDefault.objects.get(user=request.user)
    except UserDefault.DoesNotExist:
        user_defaults = None
    
    context = {
        'hours_since_last': hours_since_last,
        'minutes_since_last': minutes_since_last,
        'today_smokes': today_smokes,
        'daily_limit': daily_limit,
        'progress_percentage': progress_percentage,
        'recent_logs': recent_logs,
        'last_smoke': last_smoke,
        'user_defaults': user_defaults,
    }
    
    return render(request, 'tracker/home.html', context)

@login_required
def log_smoke(request):
    if request.method == 'POST':
        form = SmokeLogForm(request.POST)
        form.fields['user_brand'].queryset = UserBrand.objects.filter(user=request.user)
        if form.is_valid():
            smoke_log = form.save(commit=False)
            smoke_log.user = request.user
            smoke_log.save()
            messages.success(request, 'Smoke logged successfully!')
            return redirect('home')
    else:
        form = SmokeLogForm()
        form.fields['user_brand'].queryset = UserBrand.objects.filter(user=request.user)
    
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
    timezone.activate(request.user.profile.timezone)
    logs = SmokeLog.objects.filter(user=request.user)
    total_smokes = logs.count()

    if total_smokes == 0:
        return render(request, 'tracker/stats.html', {'no_data': True})

    last_smoke = logs.first()
    total_cost = logs.aggregate(total_cost=Sum('user_brand__price'))['total_cost'] or 0

    # Time-based stats
    today = timezone.now().date()
    week_ago = today - timedelta(days=7)
    month_ago = today - timedelta(days=30)

    today_logs = logs.filter(timestamp__date=today)
    week_logs = logs.filter(timestamp__date__gte=week_ago)
    month_logs = logs.filter(timestamp__date__gte=month_ago)

    today_smokes = today_logs.count()
    this_week = week_logs.count()
    this_month = month_logs.count()

    today_cost = today_logs.aggregate(total_cost=Sum('user_brand__price'))['total_cost'] or 0
    week_cost = week_logs.aggregate(total_cost=Sum('user_brand__price'))['total_cost'] or 0
    month_cost = month_logs.aggregate(total_cost=Sum('user_brand__price'))['total_cost'] or 0

    last_week = logs.filter(
        timestamp__date__gte=week_ago - timedelta(days=7),
        timestamp__date__lt=week_ago
    ).count()

    # Advanced analytics
    trigger_stats = get_trigger_stats(logs)
    trigger_labels = [item['trigger_display'] for item in trigger_stats]
    trigger_counts = [item['count'] for item in trigger_stats]
    mood_impact = get_mood_impact(logs)
    streak_info = calculate_streak(logs)

    # Daily average
    if logs.exists():
        first_log = logs.last()
        days_tracking = (timezone.now().date() - first_log.timestamp.date()).days + 1
        daily_average = round(total_smokes / days_tracking, 1)
    else:
        daily_average = 0

    # Goal limits
    try:
        daily_goal = DailyGoal.objects.get(user=request.user).daily_limit
    except DailyGoal.DoesNotExist:
        daily_goal = 0
    
    weekly_limit = daily_goal * 7 if daily_goal else 0
    monthly_limit = daily_goal * 30 if daily_goal else 0


    # Chart data
    # Daily
    daily_counts = [0] * 24
    for log in today_logs:
        local_time = log.timestamp.astimezone(timezone.get_current_timezone())
        daily_counts[local_time.hour] += 1
    daily_labels = [f"{h:02d}:00" for h in range(24)]

    # Weekly
    weekly_counts_dict = {}
    for i in range(7):
        day = today - timedelta(days=i)
        weekly_counts_dict[day.strftime('%Y-%m-%d')] = 0
    
    for log in week_logs:
        local_time = log.timestamp.astimezone(timezone.get_current_timezone())
        log_date_str = local_time.date().strftime('%Y-%m-%d')
        if log_date_str in weekly_counts_dict:
            weekly_counts_dict[log_date_str] += 1
            
    weekly_labels = [(today - timedelta(days=i)).strftime('%a') for i in range(6, -1, -1)]
    weekly_dates = [(today - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(6, -1, -1)]
    weekly_counts = [weekly_counts_dict.get(d, 0) for d in weekly_dates]

    # Monthly
    monthly_counts_dict = {}
    for i in range(4):
        week_start = today - timedelta(weeks=i)
        week_num = week_start.strftime('%W')
        monthly_counts_dict[week_num] = 0

    for log in month_logs:
        local_time = log.timestamp.astimezone(timezone.get_current_timezone())
        week_num = local_time.strftime('%W')
        if week_num in monthly_counts_dict:
            monthly_counts_dict[week_num] += 1

    last_four_weeks = [(today - timedelta(weeks=i)).strftime('%W') for i in range(3, -1, -1)]
    monthly_labels = [f"Week {w}" for w in last_four_weeks]
    monthly_counts = [monthly_counts_dict.get(w, 0) for w in last_four_weeks]

    context = {
        'total_smokes': total_smokes,
        'total_cost': total_cost,
        'last_smoke': last_smoke,
        'today_smokes': today_smokes,
        'this_week': this_week,
        'this_month': this_month,
        'today_cost': today_cost,
        'week_cost': week_cost,
        'month_cost': month_cost,
        'last_week': last_week,
        'daily_average': daily_average,
        'trigger_stats': trigger_stats,
        'trigger_labels': trigger_labels,
        'trigger_counts': trigger_counts,
        'mood_impact': mood_impact,
        'streak_info': streak_info,
        'daily_goal': daily_goal,
        'weekly_limit': weekly_limit,
        'monthly_limit': monthly_limit,
        'daily_labels': daily_labels,
        'daily_counts': daily_counts,
        'weekly_labels': weekly_labels,
        'weekly_counts': weekly_counts,
        'monthly_labels': monthly_labels,
        'monthly_counts': monthly_counts,
    }

    return render(request, 'tracker/stats.html', context)

@login_required
def brand_list(request):
    brands = UserBrand.objects.filter(user=request.user)
    return render(request, 'tracker/brand_list.html', {'brands': brands})

@login_required
def add_brand(request):
    if request.method == 'POST':
        form = UserBrandForm(request.POST, user=request.user)
        if form.is_valid():
            user_brand = form.save(commit=False)
            user_brand.user = request.user
            user_brand.save()
            messages.success(request, 'Brand added to your list successfully!')
            return redirect('brand_list')
    else:
        form = UserBrandForm(user=request.user)
    
    return render(request, 'tracker/brand_form.html', {'form': form})

@login_required
def edit_brand(request, pk):
    user_brand = get_object_or_404(UserBrand, pk=pk, user=request.user)
    if request.method == 'POST':
        form = UserBrandForm(request.POST, instance=user_brand, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Brand updated successfully!')
            return redirect('brand_list')
    else:
        form = UserBrandForm(instance=user_brand, user=request.user)
    
    return render(request, 'tracker/brand_form.html', {'form': form, 'brand': user_brand})

@login_required
def request_brand(request):
    if request.method == 'POST':
        form = BrandRequestForm(request.POST)
        if form.is_valid():
            brand_request = form.save(commit=False)
            brand_request.user = request.user
            brand_request.save()
            messages.success(request, 'Your request has been submitted for review.')
            return redirect('request_brand')
    else:
        form = BrandRequestForm()
    
    previous_requests = BrandRequest.objects.filter(user=request.user)
    return render(request, 'tracker/request_brand.html', {
        'form': form,
        'previous_requests': previous_requests
    })

@login_required
def delete_brand(request, pk):
    user_brand = get_object_or_404(UserBrand, pk=pk, user=request.user)
    if request.method == 'POST':
        user_brand.delete()
        messages.success(request, 'Brand deleted successfully!')
        return redirect('brand_list')
    
    return render(request, 'tracker/brand_confirm_delete.html', {'brand': user_brand})

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

@login_required
def set_defaults(request):
    try:
        defaults = UserDefault.objects.get(user=request.user)
    except UserDefault.DoesNotExist:
        defaults = None
    
    if request.method == 'POST':
        form = UserDefaultForm(request.POST, instance=defaults)
        form.fields['user_brand'].queryset = UserBrand.objects.filter(user=request.user)
        if form.is_valid():
            defaults = form.save(commit=False)
            defaults.user = request.user
            defaults.save()
            messages.success(request, 'Default settings updated successfully!')
            return redirect('home')
    else:
        form = UserDefaultForm(instance=defaults)
        form.fields['user_brand'].queryset = UserBrand.objects.filter(user=request.user)

    return render(request, 'tracker/set_defaults.html', {'form': form})

@login_required
def profile_settings(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your settings have been updated.')
            return redirect('profile_settings')
    else:
        form = ProfileForm(instance=request.user.profile)
    return render(request, 'tracker/profile_settings.html', {'form': form})

@login_required
def quick_log(request):
    try:
        defaults = UserDefault.objects.get(user=request.user)
        if not defaults.user_brand:
            messages.error(request, 'Please set your default brand first.')
            return redirect('set_defaults')
            
        SmokeLog.objects.create(
            user=request.user,
            user_brand=defaults.user_brand,
            trigger=defaults.trigger,
            mood_before=defaults.mood_before,
            mood_after=defaults.mood_after,
        )
        # messages.success(request, 'Quick smoke logged successfully!')
    except UserDefault.DoesNotExist:
        messages.error(request, 'Please set your default preferences first.')
        return redirect('set_defaults')
    return redirect('home')

@login_required
def setup_wizard(request, step=1):
    # Redirect user to home if setup is already complete
    if 'setup_complete' in request.session:
        return redirect('home')

    if step == 1:
        # Step 1: Set Daily Goal
        goal, created = DailyGoal.objects.get_or_create(user=request.user)
        if request.method == 'POST':
            form = DailyGoalForm(request.POST, instance=goal)
            if form.is_valid():
                form.save()
                request.session['setup_step_1_complete'] = True
                return redirect('setup_wizard', step=2)
        else:
            form = DailyGoalForm(instance=goal)
        
        return render(request, 'tracker/setup_step_1.html', {'form': form, 'step': 1})

    elif step == 2:
        # Step 2: Add a Brand
        if not request.session.get('setup_step_1_complete'):
            return redirect('setup_wizard', step=1)
        if request.method == 'POST':
            form = UserBrandForm(request.POST, user=request.user)
            if form.is_valid():
                brand = form.cleaned_data['brand']
                price = form.cleaned_data['price']
                user_brand, created = UserBrand.objects.get_or_create(
                    user=request.user,
                    brand=brand,
                    defaults={'price': price}
                )
                if created:
                    messages.success(request, 'Brand added successfully!')
                else:
                    # Optionally, update the price if the brand already exists
                    user_brand.price = price
                    user_brand.save()
                    messages.info(request, 'Brand price updated.')

                # Check if all brands have been added
                user_brand_count = UserBrand.objects.filter(user=request.user).count()
                total_brand_count = Brand.objects.count()

                if user_brand_count >= total_brand_count:
                    messages.success(request, "All available brands have been added.")
                    return redirect('setup_wizard', step=3)

                if 'add_another' in request.POST:
                    return redirect('setup_wizard', step=2)
                return redirect('setup_wizard', step=3)
        else:
            form = UserBrandForm(user=request.user)
        
        brands = UserBrand.objects.filter(user=request.user)
        return render(request, 'tracker/setup_step_2.html', {'form': form, 'brands': brands, 'step': 2})

    elif step == 3:
        # Step 3: Set Defaults
        if not request.session.get('setup_step_1_complete'):
            return redirect('setup_wizard', step=1)
        if not UserBrand.objects.filter(user=request.user).exists():
            messages.error(request, "Please add at least one brand before setting defaults.")
            return redirect('setup_wizard', step=2)

        defaults, created = UserDefault.objects.get_or_create(user=request.user)
        if request.method == 'POST':
            form = UserDefaultForm(request.POST, instance=defaults)
            form.fields['user_brand'].queryset = UserBrand.objects.filter(user=request.user)
            if form.is_valid():
                form.save()
                profile = request.user.profile
                profile.setup_complete = True
                profile.save()
                request.session['setup_complete'] = True # Keep session for immediate redirect
                messages.success(request, 'Setup complete! Welcome to Smoke Tracker.')
                return redirect('home')
        else:
            form = UserDefaultForm(instance=defaults)
            form.fields['user_brand'].queryset = UserBrand.objects.filter(user=request.user)
            
        return render(request, 'tracker/setup_step_3.html', {'form': form, 'step': 3})

    return redirect('home')


@user_passes_test(lambda u: u.is_superuser)
def approve_brand_request(request, pk):
    brand_request = get_object_or_404(BrandRequest, pk=pk)
    Brand.objects.get_or_create(name=brand_request.brand_name)
    brand_request.status = 'approved'
    brand_request.save()
    messages.success(request, f"Brand '{brand_request.brand_name}' has been approved and added to the list.")
    return redirect('admin_dashboard')

@user_passes_test(lambda u: u.is_superuser)
def reject_brand_request(request, pk):
    brand_request = get_object_or_404(BrandRequest, pk=pk)
    brand_request.status = 'rejected'
    brand_request.save()
    messages.warning(request, f"Request for brand '{brand_request.brand_name}' has been rejected.")
    return redirect('admin_dashboard')

@user_passes_test(lambda u: u.is_superuser)
def admin_dashboard(request):
    # Time-based filtering
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')

    smokelogs_query = SmokeLog.objects.all()
    if date_from:
        smokelogs_query = smokelogs_query.filter(timestamp__date__gte=date_from)
    if date_to:
        smokelogs_query = smokelogs_query.filter(timestamp__date__lte=date_to)

    total_users = User.objects.count()
    total_brands = Brand.objects.count()
    total_smokelogs = smokelogs_query.count()

    # Analytics
    if total_users > 0:
        avg_smokes_per_user = total_smokelogs / total_users
    else:
        avg_smokes_per_user = 0

    user_smoke_counts = User.objects.annotate(
        smoke_count=Count('smokelog', filter=smokelogs_query.filter(user_id__in=User.objects.all()).values('user_id'))
    ).order_by('-smoke_count')[:10]

    brand_smoke_counts = Brand.objects.annotate(
        smoke_count=Count('userbrand__smokelog', filter=smokelogs_query.filter(user_brand__brand_id__in=Brand.objects.all()).values('user_brand__brand_id'))
    ).order_by('-smoke_count')

    trigger_stats = smokelogs_query.values('trigger').annotate(count=Count('trigger')).order_by('-count')
    mood_before_stats = smokelogs_query.values('mood_before').annotate(count=Count('mood_before')).order_by('-count')
    mood_after_stats = smokelogs_query.values('mood_after').annotate(count=Count('mood_after')).order_by('-count')

    brand_requests = BrandRequest.objects.filter(status='pending')

    context = {
        'total_users': total_users,
        'total_brands': total_brands,
        'total_smokelogs': total_smokelogs,
        'user_smoke_counts': user_smoke_counts,
        'brand_smoke_counts': brand_smoke_counts,
        'brand_requests': brand_requests,
        'avg_smokes_per_user': f"{avg_smokes_per_user:.2f}",
        'trigger_stats': trigger_stats,
        'mood_before_stats': mood_before_stats,
        'mood_after_stats': mood_after_stats,
        'date_from': date_from,
        'date_to': date_to,
    }
    return render(request, 'tracker/admin_dashboard.html', context)
