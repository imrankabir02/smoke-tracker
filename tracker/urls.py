from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('dashboard/', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('log/', views.log_smoke, name='log_smoke'),
    path('logs/', views.log_list, name='log_list'),
    path('stats/', views.stats, name='stats'),
    path('achievements/', views.achievements, name='achievements'),
    path('brands/', views.brand_list, name='brand_list'),
    path('brands/add/', views.add_brand, name='add_brand'),
    path('brands/edit/<int:pk>/', views.edit_brand, name='edit_brand'),
    path('brands/delete/<int:pk>/', views.delete_brand, name='delete_brand'),
    path('brands/request/', views.request_brand, name='request_brand'),
    path('brands/request/approve/<int:pk>/', views.approve_brand_request, name='approve_brand_request'),
    path('brands/request/reject/<int:pk>/', views.reject_brand_request, name='reject_brand_request'),
    path('goal/', views.set_goal, name='set_goal'),
    path('defaults/', views.set_defaults, name='set_defaults'),
    path('settings/', views.profile_settings, name='profile_settings'),
    path('quick-log/', views.quick_log, name='quick_log'),
    path('setup/', views.setup_wizard, {'step': 1}, name='setup_start'),
    path('setup/<int:step>/', views.setup_wizard, name='setup_wizard'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
]
