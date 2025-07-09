from django.shortcuts import redirect
from django.urls import reverse
from .models import DailyGoal, UserBrand

class SetupWizardMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and hasattr(request.user, 'profile') and not request.user.profile.setup_complete:
            # Allow access to setup wizard, logout, and admin
            allowed_paths = [
                reverse('setup_start'),
                reverse('setup_wizard', args=[1]),
                reverse('setup_wizard', args=[2]),
                reverse('setup_wizard', args=[3]),
                reverse('logout'),
            ]
            
            # Allow admin access
            if request.path.startswith('/admin/'):
                return self.get_response(request)

            if request.path not in allowed_paths:
                # Redirect to the appropriate setup step
                if not DailyGoal.objects.filter(user=request.user).exists():
                     return redirect('setup_wizard', step=1)
                elif not UserBrand.objects.filter(user=request.user).exists():
                    return redirect('setup_wizard', step=2)
                else:
                    return redirect('setup_wizard', step=3)

        response = self.get_response(request)
        return response
