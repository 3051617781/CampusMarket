from django.urls import path
from .views import user_login
from .views import user_list, user_detail, user_follows
from .views import circle_list, circle_detail, circle_user_follows, circle_user_manage
from .views import post_list, post_detail, post_user_likes, post_user_collects, post_user_comments
from .views import comment_list
from .views import action_upload_img, action_create_post, action_create_comment, action_create_circle
from .views import action_update_selfinfo
from .views import action_like_post, action_like_comment, action_like_circle, action_like_user
from .views import action_collect_post, action_collect_comment, action_collect_circle
from .views import action_follow_user, action_follow_circle

urlpatterns = [
# # ====== 登录注册======
    path('login/', user_login),
#     path('exit/', user_exit),

# =======查询接口======
# 用户
    path('user/list/', user_list), # 用户列表（昵称关键词搜索、圈子过滤）
    path('user/<int:user_id>/', user_detail), # 根据用户id查询用户信息
    path('user/follows/',user_follows), # 关注的用户列表
    # path('circle/<int:circle_id>/members/', circle_members), # 圈子成员列表

# 圈子
    path('circle/list/', circle_list), # 圈子列表（关键词搜索）
    path('circle/<int:circle_id>/', circle_detail), # 根据圈子id查询圈子信息
    # 圈子-用户
    path('circle/user/follows/', circle_user_follows), # 用户关注的圈子
    path('circle/user/manage/', circle_user_manage), # 用户管理的圈子

# 帖子
    path('post/list/', post_list), # 帖子列表（关键词搜索，圈子、用户过滤）
    path('post/<int:post_id>/', post_detail), # 根据帖子id查询帖子信息
    # 帖子-用户
    path('post/user/likes/', post_user_likes), # 用户点赞的帖子
    path('post/user/collects/', post_user_collects), # 用户收藏的帖子
    path('post/user/comments/', post_user_comments), # 用户评论的帖子

# 评论
    path('comment/list/', comment_list), # 评论列表（关键词搜索、帖子过滤）
#     path('comment/<int:comment_id>/', comment_detail), # 根据评论id查询评论


# ====== 用户操作======
# 用户上传（图片）
    path('action/upload/img/', action_upload_img),# 用户上传图片

# 用户创建（帖子、评论、圈子）
    path('action/create/post/', action_create_post), # 用户创建帖子
    path('action/create/comment/', action_create_comment), # 用户创建评论
    path('action/create/circle/', action_create_circle), # 用户创建圈子

# 用户修改（帖子、个人信息、评论）
#     path('action/update/post/', action_update_post), # 用户修改帖子
#     path('action/update/comment/', action_update_comment), # 用户修改评论
    path('action/update/selfinfo/', action_update_selfinfo), # 用户修改个人信息


# 用户点赞（帖子、评论、圈子、用户）
    path('action/like/post/', action_like_post), # 用户点赞帖子
    path('action/like/comment/', action_like_comment), # 用户点赞评论
    path('action/like/circle/', action_like_circle), # 用户点赞圈子
    path('action/like/user/', action_like_user), # 用户点赞用户

# 用户收藏（帖子、评论、圈子）
    path('action/collect/post/', action_collect_post), # 用户收藏帖子
    path('action/collect/comment/', action_collect_comment), # 用户收藏评论
    path('action/collect/circle/', action_collect_circle), # 用户收藏圈子

# 用户关注（用户、圈子）
    path('action/follow/user/', action_follow_user), # 用户关注用户
    path('action/follow/circle/', action_follow_circle), # 用户关注圈子

# # 用户举报（帖子、圈子、评论、用户）
#     path('action/informant/post/', action_informant_post), # 用户举报帖子
#     path('action/informant/circle/', action_informant_circle), # 用户举报圈子
#     path('action/informant/comment/', action_informant_comment), # 用户举报评论
#     path('action/informant/user/', action_informant_user), # 用户举报用户

# # ======消息通知======
#     path('notify/comment_info/', notify_comment_info), # 评论通知
#     path('notify/reply_info/', notify_reply_info), # 回复通知
#     path('notify/like_info/', notify_like_info), # 点赞通知
#     path('notify/follow_info/', notify_follow_info), # 关注通知

]
