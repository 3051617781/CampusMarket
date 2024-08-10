from django.contrib import admin
from .models import  School, SchoolRegion, CustomUser, Circle, Post, Comment, Image
from .relations import PostImage
from .relations import Report, UserLikePost, UserLikeComment, UserLikeCircle, UserLikeUser
from .relations import UserCollectPost, UserCollectComment, UserCollectCircle
from .relations import UserFollowUser, UserFollowCircle

# Register your models here.
admin.site.register(School)
admin.site.register(SchoolRegion)
admin.site.register(CustomUser)
admin.site.register(Circle)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Image)

admin.site.register(Report)
admin.site.register(UserLikePost)
admin.site.register(UserLikeComment)
admin.site.register(UserLikeCircle)
admin.site.register(UserLikeUser)
admin.site.register(UserCollectPost)
admin.site.register(UserCollectComment)
admin.site.register(UserCollectCircle)
admin.site.register(UserFollowUser)
admin.site.register(UserFollowCircle)
admin.site.register(PostImage)
