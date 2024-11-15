# admin_portal/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.db.models import Count
from django.core.paginator import Paginator
from user.models import Post
from .models import ModeratorLog
from django.contrib.auth.views import LoginView
from account_app.forms import CustomLoginForm
from django.urls import reverse_lazy

User = get_user_model()

def is_admin(user):
    return user.is_authenticated and user.is_staff

@user_passes_test(is_admin)
def admin_dashboard(request):
    total_users = User.objects.count()
    total_posts = Post.objects.count()
    blocked_users = User.objects.filter(is_active=False).count()
    blocked_posts = Post.objects.filter(is_blocked=True).count()
    recent_actions = ModeratorLog.objects.select_related('moderator', 'target_user', 'target_post').order_by('-timestamp')[:10]

    context = {
        'total_users': total_users,
        'total_posts': total_posts,
        'blocked_users': blocked_users,
        'blocked_posts': blocked_posts,
        'recent_actions': recent_actions
    }
    return render(request, 'admin/dashboard.html', context)



@user_passes_test(is_admin)
def user_management(request):
    users = User.objects.annotate(
        post_count=Count('posts'),
        comment_count=Count('comments')
    ).order_by('-date_joined')
    
    paginator = Paginator(users, 20)
    page = request.GET.get('page')
    users = paginator.get_page(page)
    
    return render(request, 'admin/user_management.html', {'users': users})

@user_passes_test(is_admin)
def post_management(request):
    posts = Post.objects.select_related('author').annotate(
        comment_count=Count('comments'),
        like_count=Count('likes')
    ).order_by('-created_at')
    
    paginator = Paginator(posts, 20)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    
    return render(request, 'admin/post_management.html', {'posts': posts})

@user_passes_test(is_admin)
def block_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        reason = request.POST.get('reason', '')
        user.is_active = False
        user.save()
        
        ModeratorLog.objects.create(
            moderator=request.user,
            action='block_user',
            target_user=user,
            reason=reason
        )
        
        messages.success(request, f'User {user.username} has been blocked.')
    return redirect('admin_user_management')

@user_passes_test(is_admin)
def unblock_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.is_active = True
    user.save()
    
    ModeratorLog.objects.create(
        moderator=request.user,
        action='unblock_user',
        target_user=user,
        reason='Unblocked by admin'
    )
    
    messages.success(request, f'User {user.username} has been unblocked.')
    return redirect('admin_user_management')

@user_passes_test(is_admin)
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        reason = request.POST.get('reason', '')
        username = user.username
        
        ModeratorLog.objects.create(
            moderator=request.user,
            action='delete_user',
            reason=f'Deleted user: {username} - {reason}'
        )
        
        user.delete()
        messages.success(request, f'User {username} has been deleted.')
    return redirect('admin_user_management')

@user_passes_test(is_admin)
def block_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        reason = request.POST.get('reason', '')
        post.is_blocked = True
        post.save()
        
        ModeratorLog.objects.create(
            moderator=request.user,
            action='block_post',
            target_post=post,
            reason=reason
        )
        
        messages.success(request, f'Post "{post.title}" has been blocked.')
    return redirect('admin_post_management')

@user_passes_test(is_admin)
def unblock_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.is_blocked = False
    post.save()
    
    ModeratorLog.objects.create(
        moderator=request.user,
        action='unblock_post',
        target_post=post,
        reason='Unblocked by admin'
    )
    
    messages.success(request, f'Post "{post.title}" has been unblocked.')
    return redirect('admin_post_management')

@user_passes_test(is_admin)
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        reason = request.POST.get('reason', '')
        title = post.title
        
        ModeratorLog.objects.create(
            moderator=request.user,
            action='delete_post',
            reason=f'Deleted post: {title} - {reason}'
        )
        
        post.delete()
        messages.success(request, f'Post "{title}" has been deleted.')
    return redirect('admin_post_management')

@user_passes_test(is_admin)
def moderation_logs(request):
    logs = ModeratorLog.objects.select_related(
        'moderator', 'target_user', 'target_post'
    ).order_by('-timestamp')
    
    paginator = Paginator(logs, 50)
    page = request.GET.get('page')
    logs = paginator.get_page(page)
    
    return render(request, 'admin/moderation_logs.html', {'logs': logs})


