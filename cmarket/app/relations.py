# 关系模型

from django.db import models
from .models import  CustomUser, School, SchoolRegion, Circle, Post, Comment, Image

"""帖子图片"""
class PostImage(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_images')
    image = models.ForeignKey(Image, on_delete=models.CASCADE, related_name='post_images')
    # 额外排序字段
    order = models.PositiveIntegerField(default=0)

    class Meta:
        # 确保图片的顺序是按照升序排列的
        ordering = ['order']
        # 确保不会有重复的帖子-图片对
        unique_together = ('post', 'image')

"""用户举报（帖子、圈子、评论、用户）"""
class Report(models.Model):
    id = models.BigAutoField(primary_key=True)
    report_type = models.CharField(max_length=50, choices=[('post', '帖子'), ('circle', '圈子'), ('comment', '评论'), ('user', '用户')], verbose_name='举报类型')
    reason = models.TextField(verbose_name='举报理由', null=True, blank=True)
    status = models.CharField(max_length=50, choices=[('pending', '待处理'), ('approved', '已批准'), ('rejected', '已拒绝')], default='pending', verbose_name='举报状态')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    reporter = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='reports', verbose_name='举报者')
    reported_object = models.ForeignKey(Post if report_type == 'post' else Circle if report_type == 'circle' else Comment if report_type == 'comment' else CustomUser, on_delete=models.CASCADE, related_name='reporters', verbose_name='被举报对象')

    def __str__(self):
        if self.report_type == 'post':
            return f"{self.reporter.nickname}:id({self.reporter.id})举报了帖子{self.reported_object.title}:id({self.reported_object.id})"
        elif self.report_type == 'circle':
            return f"{self.reporter.nickname}:id({self.reporter.id})举报了{self.reported_object.name}:id({self.reported_object.id})"
        elif self.report_type == 'comment':
            return f"{self.reporter.nickname}:id({self.reporter.id})举报了{self.reported_object.content}:id({self.reported_object.id})"
        elif self.report_type == 'user':
            return f"{self.reporter.nickname}:id({self.reporter.id})举报了用户{self.reported_object.nickname}:id({self.reported_object.id})"

"""用户点赞（帖子、评论、圈子、用户）"""
class UserLikePost(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='liked_posts')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likers')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='点赞时间')

    class Meta:
        unique_together = ('user', 'post')

    def __str__(self):
        return f"{self.user.nickname} 点赞了 {self.post.title}"

class UserLikeComment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='liked_comments')
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='likers')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='点赞时间')

    class Meta:
        unique_together = ('user', 'comment')

    def __str__(self):
        return f"{self.user.nickname} 点赞了 {self.comment.content}"

class UserLikeCircle(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='liked_circles')
    circle = models.ForeignKey(Circle, on_delete=models.CASCADE, related_name='likers')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='点赞时间')

    class Meta:
        unique_together = ('user', 'circle')

    def __str__(self):
        return f"{self.user.nickname} 点赞了 {self.circle.name}"

class UserLikeUser(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='liked_users')
    liked_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='likers')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='点赞时间')

    class Meta:
        unique_together = ('user', 'liked_user')

    def __str__(self):
        return f"{self.user.nickname} 点赞了 {self.liked_user.nickname}"


"""用户收藏（帖子、圈子、评论）"""
class UserCollectPost(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='collected_posts')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='collecters')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='收藏时间')

    class Meta:
        unique_together = ('user', 'post')

    def __str__(self):
        return f"{self.user.nickname} 收藏了 {self.post.title}"

class UserCollectCircle(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='collected_circles')
    circle = models.ForeignKey(Circle, on_delete=models.CASCADE, related_name='collecters')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='收藏时间')

    class Meta:
        unique_together = ('user', 'circle')

    def __str__(self):
        return f"{self.user.nickname} 收藏了 {self.circle.name}"

class UserCollectComment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='collected_comments')
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='collecters')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='收藏时间')

    class Meta:
        unique_together = ('user', 'comment')

    def __str__(self):
        return f"{self.user.nickname} 收藏了 {self.comment.content}"


"""用户关注（用户、圈子）"""
class UserFollowUser(models.Model):
    follower = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='following_users')
    following = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='关注时间')

    class Meta:
        unique_together = ('follower', 'following')  # 确保关注关系是唯一的，防止重复关注

    def __str__(self):
        return f"{self.follower.nickname} 关注 {self.following.nickname}"

class UserFollowCircle(models.Model):
    follower = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='following_circles')
    following = models.ForeignKey(Circle, on_delete=models.CASCADE, related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='关注时间')

    class Meta:
        unique_together = ('follower', 'following')

    def __str__(self):
        return f"{self.follower.nickname} 关注 {self.following.name}"

