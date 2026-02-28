"""
URL configuration for my_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from login_view import views
from django.conf.urls.static import static
from django.conf import settings
import os

urlpatterns = [
    path('', views.login_view, name='login'), 
    path('register/', views.register_view, name='register'), 
    path('logout/', views.logout_view, name='logout'),
    path('home/', views.index, name='home'),
    path('search/', views.index, name='search'),
    path('forgot-password/', views.forgot_password_view, name='password_reset'),
    path('password-reset-confirm/', views.password_reset_confirm_view, name='password_reset_confirm'),
    path('upload/', views.upload_image_view, name='upload_image'),
    path('profile/', views.profile_view, name='profile'),
    path('admin-panel/', views.admin_dashboard_view, name='admin_dashboard'),
    path('admin-manage/', views.manage_members_view, name='admin_manage'),
    path('approve/<int:image_id>/', views.approve_image_view, name='approve_image'),
    path('reject/<int:image_id>/', views.reject_image_view, name='reject_image'),
] + static(settings.STATIC_URL, document_root=os.path.join(settings.BASE_DIR, 'static'))

