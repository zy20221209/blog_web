from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'blog'
urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_create, name='post_create'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('post/<int:pk>/delete/', views.post_delete, name='post_delete'),
    path('comment/<int:pk>/add/', views.add_comment, name='add_comment'),
]

# 只在 DEBUG=True 时生效（开发环境）
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    # 如果你有上传的媒体文件，也加上：
    # urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)