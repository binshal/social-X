from django.urls import path
from . import views

urlpatterns = [
    path('adminview/', views.admin_dashboard, name='admin_dashboard'),
    path('users/', views.user_management, name='admin_user_management'),
    path('posts/', views.post_management, name='admin_post_management'),
    path('logs/', views.moderation_logs, name='moderation_logs'),
    

    
    # User actions
    path('users/<int:user_id>/block/', views.block_user, name='block_user'),
    path('users/<int:user_id>/unblock/', views.unblock_user, name='unblock_user'),
    path('users/<int:user_id>/delete/', views.delete_user, name='delete_user'),
    
    # Post actions
    path('posts/<int:post_id>/block/', views.block_post, name='block_post'),
    path('posts/<int:post_id>/unblock/', views.unblock_post, name='unblock_post'),
    path('posts/<int:post_id>/delete/', views.delete_post, name='delete_post'),
    
]

