from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.validators import FileExtensionValidator

# Create your models here.
class Post(models.Model):
    POST_TYPES = (
        ('blog','Blog Post'),
        ('image','Image Post'),
    )
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True)
    post_type = models.CharField(max_length=5,choices=POST_TYPES)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_blocked = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    # image specific fields
    image = models.ImageField(
        upload_to='post_images',
        null = True,
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg','jpeg','png','gif'])],
    )
    image_caption = models.CharField(max_length=500,blank=True)

    def __str__(self):
        return f"{self.get_post_type_display()}: {self.title}"
    
    def soft_delete(self):
        self.is_deleted = True
        self.save()
        # self.send_notification_email('deleted')

    def block(self):
        self.is_blocked = True
        self.save()
        # self.send_notification_email('blocked')
    
    def send_notification_email(self,action):
        from django.core.mail import send_mail
        subject = f"your {self.get_post_type_display().lower()} has been {action}"
        message = f"your {self.get_post_type_display().lower()} '{self.title}' has been {action} by the admin."
        from_email = 'noreply@socialx.com'
        recipient_list = [self.author.email]
        send_mail(subject,message,from_email,recipient_list)

class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_blocked = models.BooleanField(default=False)

    def __str__(self):
        return f"comment by {self.author.username} on {self.post.title}"
    
class Like(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='likes')
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('post','user')

    def __str__(self):
        return f'liked by {self.user.username} on {self.post.title}'