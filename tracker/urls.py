from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('log/', views.log_smoke, name='log_smoke'),
    path('logs/', views.log_list, name='log_list'),
    path('stats/', views.stats, name='stats'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('brands/', views.brand_list, name='brand_list'),
    path('add-brand/', views.add_brand, name='add_brand'),
    path('edit-brand/<int:pk>/', views.edit_brand, name='edit_brand'),
    path('delete-brand/<int:pk>/', views.delete_brand, name='delete_brand'),
    path('set-goal/', views.set_goal, name='set_goal'),
    path('set-defaults/', views.set_defaults, name='set_defaults'),
    path('quick-log/', views.quick_log, name='quick_log'),
    path('signup/', views.signup, name='signup'),
    path('profile/', views.profile_settings, name='profile_settings'),
    path('setup/', views.setup_wizard, name='setup_start'),
    path('setup/<int:step>/', views.setup_wizard, name='setup_wizard'),
]
