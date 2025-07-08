from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('log/', views.log_smoke, name='log_smoke'),
    path('logs/', views.log_list, name='log_list'),
    path('stats/', views.stats, name='stats'),
    path('signup/', views.signup, name='signup'),
    path('add-brand/', views.add_brand, name='add_brand'),
    path('brands/', views.brand_list, name='brand_list'),
]
