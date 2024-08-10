from django.db import models
import uuid

# 学校
class School(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, verbose_name='学校名称')

    def __str__(self):
        return self.name

# 学校校区
class SchoolRegion(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, verbose_name='校区名称')

    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='regions', verbose_name='所属学校')

    def __str__(self):
        return f"{self.school.name} {self.name}"

# 用户
class CustomUser(models.Model):
    wechat_openid = models.CharField(max_length=255, unique=True, verbose_name='微信OpenID', null=True, blank=True)
    id = models.BigAutoField(primary_key=True, editable=False)
    nickname = models.CharField(null=True, blank=True, max_length=50, verbose_name='昵称')

    avatar = models.URLField(null=True, blank=True, verbose_name='头像URL')
    phone = models.CharField(null=True, blank=True, max_length=11, unique=True, verbose_name='手机号')
    gender = models.CharField(null=True, blank=True, max_length=10, choices=(('male', '男'), ('female', '女'),('unknow','未知')), verbose_name='性别')
    signature = models.CharField(null=True, blank=True, max_length=200, verbose_name='个性签名')
    email = models.EmailField(null=True, blank=True, unique=True, verbose_name='邮箱')
    birthday = models.DateField(null=True, blank=True, verbose_name='生日')
    height = models.IntegerField(null=True, blank=True, verbose_name='身高')
    background_image = models.URLField(null=True, blank=True, verbose_name='背景图URL')
    hometown = models.CharField(null=True, blank=True, max_length=50, verbose_name='家乡')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    is_verified = models.BooleanField(default=False, verbose_name='是否通过认证')
    is_frozen = models.BooleanField(default=False, verbose_name='是否冻结')

    school = models.ForeignKey('School', on_delete=models.CASCADE, related_name='students', verbose_name='所在学校', null=True, blank=True)
    region = models.ForeignKey('SchoolRegion', on_delete=models.CASCADE, related_name='students', verbose_name='所在校区', null=True, blank=True)

    like_number = models.IntegerField(default=0, verbose_name='点赞数')
    fan_number = models.IntegerField(default=0, verbose_name='粉丝数') # 用户被关注
    follow_number = models.IntegerField(default=0, verbose_name='关注数') # 用户关注数

    def __str__(self):
        return self.nickname


# 圈子
class Circle(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, verbose_name='圈子名称')
    description = models.TextField(verbose_name='圈子描述')
    avatar = models.URLField(verbose_name='圈子头像URL')

    notice = models.TextField(null=True, blank=True, verbose_name='圈子公告')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    is_verified = models.BooleanField(default=False, verbose_name='是否通过认证')
    is_frozen = models.BooleanField(default=False, verbose_name='是否冻结')

    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='circles', verbose_name='创建者')
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='circles', verbose_name='所属学校')

    like_number = models.IntegerField(default=0, verbose_name='点赞数')
    collect_number = models.IntegerField(default=0, verbose_name='收藏数')
    fan_number = models.IntegerField(default=0, verbose_name='粉丝数')

    def __str__(self):
        return f"{self.name} (创建者：{self.creator.nickname})"

# 帖子
class Post(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=200, verbose_name='标题') 
    content = models.TextField(verbose_name='内容')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    is_frozen = models.BooleanField(default=False, verbose_name='是否冻结')

    circle = models.ForeignKey(Circle, on_delete=models.CASCADE, related_name='posts', verbose_name='所属圈子')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='posts', verbose_name='作者')

    like_number = models.IntegerField(default=0, verbose_name='点赞数')
    collect_number = models.IntegerField(default=0, verbose_name='收藏数')
    comment_number = models.IntegerField(default=0, verbose_name='评论数')

    def __str__(self):
        return f"{self.author.nickname}发布的{self.title}"
    

# 评论
class Comment(models.Model):
    id = models.BigAutoField(primary_key=True)
    content = models.TextField(verbose_name='评论内容')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name='所属帖子')
    reply_to = models.ForeignKey('self', on_delete=models.SET_NULL,  related_name='replies', verbose_name='回复目标', null=True, blank=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='comments', verbose_name='作者')

    like_number = models.IntegerField(default=0, verbose_name='点赞数')
    reply_number = models.IntegerField(default=0, verbose_name='回复数')

    def __str__(self):
        return f"{self.author.nickname}的{self.content}"

    def delete(self, *args, **kwargs):
        # 当删除一个评论时，将指向它的所有回复评论的reply_to字段设置为NULL
        if self.reply_to:
            self.reply_to.replies.update(reply_to=None)
        super().delete(*args, **kwargs)


# 通知
class Notification(models.Model):
    id = models.BigAutoField(primary_key=True)
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_notifications', verbose_name='事件发送者')
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='notifications', verbose_name='接收用户')
    content = models.TextField(verbose_name='通知内容', null=True, blank=True)
    status = models.BooleanField(default=False, verbose_name='状态')  # True 表示已读，False 表示未读
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

# 上传的图片
class Image(models.Model):
    id = models.BigAutoField(primary_key=True)
    image = models.CharField(max_length=255, verbose_name='图片url')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    uploader = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='images', verbose_name='上传者')

