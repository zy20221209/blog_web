# blog/models.py

from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(Tag, blank=True)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.pk})

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'Comment by {self.author.username} on {self.post.title}'
    

class PostView(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='views')
    session_id = models.CharField(max_length=100, blank=True, null=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # 确保同一个 session 或 IP 不会重复计数
        unique_together = ('post', 'session_id')
        verbose_name = "文章阅读记录"
        verbose_name_plural = "文章阅读记录"

    def __str__(self):
        return f"{self.post.title} 被阅读"
    


# class PostReaction(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     post = models.ForeignKey(Post, on_delete=models.CASCADE)
#     reaction_type = models.CharField(
#         max_length=10,
#         choices=[
#             ('like', '赞'),
#             ('dislike', '踩'),
#         ]
#     )
#     created_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         # 确保一个用户对一篇文章只能有一种反应（点赞或点踩）
#         unique_together = ('user', 'post')
#         verbose_name = "文章反应"
#         verbose_name_plural = "文章反应"
#         # 可选：按时间倒序
#         ordering = ['-created_at']

#     def __str__(self):
#         return f"{self.user.username} {self.get_reaction_type_display()} {self.post.title}"