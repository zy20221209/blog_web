from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib import admin

app_name = 'accounts'
urlpatterns = [

    path('register/', views.register, name='register'),
    # 登录路由
    path('login/', auth_views.LoginView.as_view(
        template_name='login.html',
        redirect_authenticated_user=True  # 已登录用户不能访问登录页
    ), name='login'),
    # 登出路由
    path('logout/', auth_views.LogoutView.as_view(
        ), name='logout'),
    
]