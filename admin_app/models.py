from django.db import models
from django.contrib.auth import get_user_model
from user.models import Post
from django.utils import timezone

User = get_user_model()

class ModeratorLog(models.Model):
    ACTION_CHOICES = (
        ('block_user', 'Block User'),
        ('unblock_user', 'Unblock User'),
        ('delete_user', 'Delete User'),
        ('block_post', 'Block Post'),
        ('unblock_post', 'Unblock Post'),
        ('delete_post', 'Delete Post'),
    )

    moderator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='moderator_actions')
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    target_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='moderation_logs')
    target_post = models.ForeignKey(Post, on_delete=models.SET_NULL, null=True, blank=True, related_name='moderation_logs')
    reason = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        target = self.target_user.username if self.target_user else self.target_post.title
        return f"{self.moderator.username} - {self.action} - {target}"