from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('feed/',views.feed,name='feed'),
    path('blog/new/',views.create_blog_post,name='create_blog_post'),
    path('image/new/',views.create_image_post,name='create_image_post'),
    path('post/<int:pk>/detail',views.post_detail,name='post_detail'),
    path('blog/<int:pk>/edit/', views.edit_post, name='edit_post'),
    path('post/<int:pk>/delete/',views.delete_post,name='delete_post'),
    path('post/<int:pk>/comment',views.add_comment,name='add_comment'),
    path('post/<int:pk>/like/',views.toggle_like,name='toggle_like'),
    path('user/<str:username>/post',views.user_posts,name='user_posts'),
    

]
