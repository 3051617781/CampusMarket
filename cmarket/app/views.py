from django.shortcuts import render
import requests
from cmarket import settings
import uuid

# 模型导入
from .models import  School, SchoolRegion, CustomUser, Circle, Post, Comment, Image
from .relations import PostImage
from .relations import Report, UserLikePost, UserLikeComment, UserLikeCircle, UserLikeUser
from .relations import UserCollectPost, UserCollectComment, UserCollectCircle
from .relations import UserFollowUser, UserFollowCircle

# 前端返回模型
from .resfront import  res_user_list, res_user_detail
from .resfront import  res_circle_list, res_circle_detail
from .resfront import  res_post_list, res_post_detail

# json处理
import json

# csrf
from django.views.decorators.csrf import csrf_exempt

# jwt登录验证
from utils.jwt import generate_jwt_token  # 生成jwt
from utils.decorators import jwt_required

# 返回结果处理
from utils.results import result, err
from django.http import JsonResponse
from django.db.models import Q

# 腾讯云cos
from qcloud_cos import CosConfig, CosS3Client



"""=======登录注册======"""
def get_login_info(code):
    code_url = settings.code2Session.format(settings.AppId, settings.AppSecret, code)
    response = requests.get(code_url)
    json_response = response.json() # 把它变成json的字典
    if json_response.get("session_key"):
        return json_response
    else:
        return False


@csrf_exempt
def user_login(request):
    data = json.loads(request.body)
    code = data.get('code')
    user_data = get_login_info(code)
    if user_data:
        wechat_openid = user_data.get('openid')
        has_user = CustomUser.objects.filter(wechat_openid=wechat_openid)
        # 没有用户则创建
        if not has_user:
            user = CustomUser.objects.create(
                wechat_openid=wechat_openid,
                # 随机昵称字符串
                nickname='昵称 '+str(uuid.uuid4())[:8],
                )
            CustomUser.objects.update()
        user = CustomUser.objects.get(wechat_openid=user_data.get('openid'))

        token = generate_jwt_token(user)
        return result({
            'token': token
        })
    else:
        return err('error login!')


@csrf_exempt  # 不使用CSRF保护
def user_login_without(request):
    user_id = request.POST.get('user_id')
    user = CustomUser.objects.get(id=user_id)
    token = generate_jwt_token(user)
    return result({
        'token': token
    })

def user_exit(request):
    pass

"""=======查询接口======"""
"""用户"""
# 用户列表（昵称关键词搜索、圈子过滤）
def user_list(request):
    keyword = request.GET.get('keyword')
    circle_id = request.GET.get('circle_id')

    query = CustomUser.objects.all()
    
    if keyword: # 根据昵称进行关键词匹配
        query = query.filter(Q(nickname__icontains=keyword)) 

    if circle_id: # 获取关注了指定圈子ID的用户列表
        circle_followers = UserFollowCircle.objects.filter(following__id=circle_id).values_list('follower__id', flat=True)
        query = query.filter(id__in=circle_followers)

    return result({
        'count': query.count(),
        'users': res_user_list(query)
    })


# 根据用户id查询用户信息
def user_detail(request, user_id):
    user = CustomUser.objects.select_related('school', 'region').get(id=user_id)
    return result(res_user_detail(user))



# 关注的用户列表
@jwt_required
def user_follows(request):
    user = CustomUser.objects.get(id=request.user_id)

    # 查询用户关注的用户列表
    followed_users = UserFollowUser.objects.filter(follower=user).values_list('following__id', flat=True)
    # 获取关注用户的详细信息
    users_info = CustomUser.objects.filter(id__in=followed_users)

    return JsonResponse({
        'count': len(users_info), 
        'users': res_user_list(users_info),
    })

# 圈子成员列表
def circle_members():
    pass

"""圈子"""
# 圈子列表（关键词搜索）
def circle_list(request):
    keyword = request.GET.get('keyword')
    page = request.GET.get('page')
    limit = request.GET.get('limit')

    # 查询圈子列表
    query = Circle.objects.all()
    if keyword: # 根据关键词进行关键词匹配
        query = query.filter(Q(name__icontains=keyword)) 
    if page and limit: # 分页
        query = query[(int(page)-1)*int(limit):int(page)*int(limit)]

    return result({
        'count': query.count(), 
        'circles': res_circle_list(query)
    })

# 根据圈子id查询圈子信息
def circle_detail(request, circle_id):
    circle = Circle.objects.get(id=circle_id)

    return result(res_circle_detail(circle))
    

# 圈子-用户
# 用户关注的圈子
@jwt_required
def circle_user_follows(request):
    user = CustomUser.objects.get(id=request.user_id)

    # 查询用户关注的圈子列表
    followed_circles = UserFollowCircle.objects.filter(follower=user).values_list('following__id', flat=True)
    # 获取关注圈子的详细信息
    circles_info = Circle.objects.filter(id__in=followed_circles)

    return result({
        'count': len(circles_info), 
        'circles': res_circle_list(circles_info)
    })

# 用户创建的圈子
@jwt_required
def circle_user_manage(request):
    user = CustomUser.objects.get(id=request.user_id)
    
    # 查询用户创建的圈子列表
    created_circles = Circle.objects.filter(creator=user).values_list('id', flat=True)
    # 获取创建圈子的详细信息
    circles_info = Circle.objects.filter(id__in=created_circles)
    
    return result({
        'count': len(circles_info), 
        'circles': res_circle_list(circles_info)
    })
    


"""帖子"""
# 帖子列表（关键词搜索，圈子、用户过滤）
def post_list(request):
    keyword = request.GET.get('keyword')
    page = request.GET.get('page')
    limit = request.GET.get('limit')
    circle_id = request.GET.get('circle_id')
    user_id = request.GET.get('user_id')

    query = Post.objects.all()
    if keyword: # 根据关键词进行关键词匹配
        query = query.filter(Q(title__icontains=keyword)) 
    if circle_id: # 获取指定圈子ID的帖子列表
        query = query.filter(circle__id=circle_id)
    if user_id: # 获取指定用户ID的帖子列表
        query = query.filter(user__id=user_id)
    if page and limit: # 分页
        query = query[(int(page)-1)*int(limit):int(page)*int(limit)]

    return result({
        'count': query.count(), 
        'posts': res_post_list(query)
    })

# 根据帖子id查询帖子信息
def post_detail(request, post_id):
    post = Post.objects.get(id=post_id)

    return result(res_post_detail(post))

# 帖子-用户
# 用户点赞的帖子
@jwt_required
def post_user_likes(request):
    user = CustomUser.objects.get(id=request.user_id)
    
    liked_posts = UserLikePost.objects.filter(user=user).values_list('post__id', flat=True)
    posts_info = Post.objects.filter(id__in=liked_posts)

    return result({
        'count': len(posts_info), 
        'posts': res_post_list(posts_info)
    })

# 用户收藏的帖子
@jwt_required
def post_user_collects(request):
    user = CustomUser.objects.get(id=request.user_id)
    
    collected_posts = UserCollectPost.objects.filter(user=user).values_list('post__id', flat=True)
    posts_info = Post.objects.filter(id__in=collected_posts)
    
    return result({
        'count': len(posts_info), 
        'posts': res_post_list(posts_info)
    })

# 用户评论的帖子
@jwt_required
def post_user_comments(request):
    user = CustomUser.objects.get(id=request.user_id)
    
    commented_posts = Comment.objects.filter(user=user).values_list('post__id', flat=True)
    posts_info = Post.objects.filter(id__in=commented_posts)

    return result({
        'count': len(posts_info), 
        'posts': res_post_list(posts_info)
    })

"""评论"""
# 评论列表（帖子搜索，发布评论用户id过滤）
def comment_list(request):
    page = request.GET.get('page')
    limit = request.GET.get('limit')
    post_id = request.GET.get('post_id')
    user_id = request.GET.get('user_id')

    query = Comment.objects.all()
    if post_id: # 根据帖子id进行帖子匹配
        query = query.filter(post__id=post_id)
    if user_id: # 根据用户id进行用户匹配
        query = query.filter(user__id=user_id)
    if page and limit: # 分页
        query = query[(int(page)-1)*int(limit):int(page)*int(limit)]

    return result({
        'count': query.count(), 
        'comments': res_comment_list(query)
    })


# 根据评论id查询评论
def comment_detail():
    pass

"""======= 用户操作======"""
"""用户上传（图片）"""
# 用户上传图片
@csrf_exempt
@jwt_required
def action_upload_img(request):
    user = CustomUser.objects.get(id=request.user_id)
    # 腾讯云cos存储返回url
    file = request.FILES['img']
    file_name = file.name
    # 生成唯一的文件名
    unique_file_name = f"{uuid.uuid4().hex}_{file_name}"

    config = CosConfig(Region=settings.TENCENT_CLOUD_REGION, SecretId=settings.TENCENT_CLOUD_SECRET_ID, SecretKey=settings.TENCENT_CLOUD_SECRET_KEY)
    client = CosS3Client(config)

    response = client.put_object(Bucket=settings.TENCENT_CLOUD_BUCKET, Body=file, Key=unique_file_name)
    response_url = f'https://{settings.TENCENT_CLOUD_BUCKET}.cos.{settings.TENCENT_CLOUD_REGION}.myqcloud.com/{unique_file_name}'
    # Image添加数据库记录
    image = Image.objects.create(
        image=response_url,
        uploader=user
    )
    return result({'url': response_url})


"""用户创建（帖子、评论、圈子）"""
# 用户创建帖子
@csrf_exempt
@jwt_required
def action_create_post(request):
    user = CustomUser.objects.get(id=request.user_id)
    data = json.loads(request.body)
    title = data.get('title')
    content = data.get('content')
    images = data.get('images', [])
    circle_id = data.get('circle_id')
    # 创建帖子
    post = Post.objects.create(
        title=title,
        content=content,
        circle_id=circle_id,
        author_id = user.id
    )
    # 处理图片
    for index, image_url in enumerate(images):
        # 创建或获取图片对象
        image, created = Image.objects.get_or_create(image=image_url)
        # 创建PostImage对象来关联帖子和图片
        PostImage.objects.create(
            post=post,
            image=image,
            order=index  # 使用索引作为排序字段的值
        )
    return result({'post_id': post.id})
    

# 用户创建评论
@csrf_exempt
@jwt_required
def action_create_comment(request):
    user = CustomUser.objects.get(id=request.user_id)
    data = json.loads(request.body)
    post_id = data.get('post_id')
    content = data.get('content')
    reply_to_id = data.get('reply_to_id')
    # 创建评论
    comment = Comment.objects.create(
        post_id=post_id,
        content=content,
        user_id=user.id,
        reply_to_id=reply_to_id
    )
    return result({'comment_id': comment.id})

# 用户创建圈子
@csrf_exempt
@jwt_required
def action_create_circle():
    user = CustomUser.objects.get(id=request.user_id)
    data = json.loads(request.body)
    avatar = data.get('avatar')
    name = data.get('name')
    description = data.get('description')

    # 用户创建的圈子所属学校要和自己所在学校一致
    # user_school = user.school
    # if user_school.id != school_id:
    #     return err('圈子所属学校与用户学校不符')
    school_id = user.school.id

    # 创建圈子
    circle = Circle.objects.create(
        avatar=avatar,
        name=name,
        description=description,
        creator_id=user.id,
        school_id=school_id
    )
    return result({'circle_id': circle.id})


"""用户修改（帖子、个人信息、评论）"""
# 用户修改帖子
def action_update_post():
    pass

# 用户修改评论
def action_update_comment():
    pass

# 用户修改个人信息
@csrf_exempt
@jwt_required
def action_update_selfinfo():
    user = CustomUser.objects.get(id=request.user_id)
    data = json.loads(request.body)
    # 提取需要更新的字段
    fields_to_update = ['phone', 'gender', 'avatar', 'nickname', 'signature', 'email', 'birthday', 'height', 'background_image', 'hometown']
    update_data = {field: data.get(field) for field in fields_to_update if field in data}

    # 更新用户信息
    for field, value in update_data.items():
        setattr(user, field, value)
    user.save()
    return result({})

"""用户点赞（帖子、评论、圈子、用户）"""
# 用户点赞帖子
@csrf_exempt
@jwt_required
def action_like_post(request):
    user = CustomUser.objects.get(id=request.user_id)
    data = json.loads(request.body)
    post_id = data.get('post_id')
    # action_type = 1 点赞 0 取消点赞
    action_type = data.get('type')
    # 创建或获取UserLikePost对象
    user_like_post, created = UserLikePost.objects.get_or_create(user=user, post_id=post_id)
    # 更新点赞状态
    if action_type == '0':
        user_like_post.delete()
    else:
        user_like_post.save()
    # 更新帖子点赞数
    post = Post.objects.get(id=post_id)
    post.like_number = post.like_number + 1 if action_type == '1' else post.like_number - 1
    post.save()

    return result({})

# 用户点赞评论
@csrf_exempt
@jwt_required
def action_like_comment(request):
    user = CustomUser.objects.get(id=request.user_id)
    data = json.loads(request.body)
    comment_id = data.get('comment_id')
    # action_type = 1 点赞 0 取消点赞
    action_type = data.get('type')
    # 创建或获取UserLikeComment对象
    user_like_comment, created = UserLikeComment.objects.get_or_create(user=user, comment_id=comment_id)
    # 更新点赞状态
    if action_type == '0':
        user_like_comment.delete()
    else:
        user_like_comment.save()
    # 更新评论点赞数
    comment = Comment.objects.get(id=comment_id)
    comment.like_number = comment.like_number + 1 if action_type == '1' else comment.like_number - 1
    comment.save()
    return result({})

# 用户点赞圈子
@csrf_exempt
@jwt_required
def action_like_circle(request):
    user = CustomUser.objects.get(id=request.user_id)
    data = json.loads(request.body)
    circle_id = data.get('circle_id')
    # action_type = 1 点赞 0 取消点赞
    action_type = data.get('type')
    # 创建或获取UserLikeCircle对象
    user_like_circle, created = UserLikeCircle.objects.get_or_create(user=user, circle_id=circle_id)
    # 更新点赞状态
    if action_type == '0':
        user_like_circle.delete()
    else:
        user_like_circle.save()
    # 更新圈子点赞数
    circle = Circle.objects.get(id=circle_id)
    circle.like_number = circle.like_number + 1 if action_type == '1' else circle.like_number - 1
    circle.save()
    return result({})

# 用户点赞用户
@csrf_exempt
@jwt_required
def action_like_user(request):
    user = CustomUser.objects.get(id=request.user_id)
    data = json.loads(request.body)
    user_id = data.get('user_id')
    # action_type = 1 关注 0 取消关注
    action_type = data.get('type')
    # 创建或获取UserLikeUser对象
    user_like_user, created = UserLikeUser.objects.get_or_create(user=user, liked_user_id=user_id)
    # 更新点赞状态
    if action_type == '0':
        user_like_user.delete()
    else:
        user_like_user.save()
    # 更新用户点赞数
    user = CustomUser.objects.get(id=user_id)
    user.like_number = user.like_number + 1 if action_type == '1' else user.like_number - 1
    user.save()
    return result({})

"""用户收藏（帖子、评论、圈子）"""
# 用户收藏帖子
@csrf_exempt
@jwt_required
def action_collect_post(request):
    user = CustomUser.objects.get(id=request.user_id)
    data = json.loads(request.body)
    post_id = data.get('post_id')
    # action_type = 1 收藏 0 取消收藏
    action_type = data.get('type')
    # 创建或获取UserCollectPost对象
    user_collect_post, created = UserCollectPost.objects.get_or_create(user=user, post_id=post_id)
    # 更新收藏状态
    if action_type == '0':
        user_collect_post.delete()
    else:
        user_collect_post.save()
    # 更新帖子收藏数
    post = Post.objects.get(id=post_id)
    post.collect_number = post.collect_number + 1 if action_type == '1' else post.collect_number - 1
    post.save()
    return result({})

# 用户收藏评论
@csrf_exempt
@jwt_required
def action_collect_comment(request):
    user = CustomUser.objects.get(id=request.user_id)
    data = json.loads(request.body)
    comment_id = data.get('comment_id')
    # action_type = 1 收藏 0 取消收藏
    action_type = data.get('type')
    # 创建或获取UserCollectComment对象
    user_collect_comment, created = UserCollectComment.objects.get_or_create(user=user, comment_id=comment_id)
    # 更新收藏状态
    if action_type == '0':
        user_collect_comment.delete()
    else:
        user_collect_comment.save()
    # 更新评论收藏数
    comment = Comment.objects.get(id=comment_id)
    comment.collect_number = comment.collect_number + 1 if action_type == '1' else comment.collect_number - 1
    comment.save()
    return result({})

# 用户收藏圈子
@csrf_exempt
@jwt_required
def action_collect_circle(request):
    user = CustomUser.objects.get(id=request.user_id)
    data = json.loads(request.body)
    circle_id = data.get('circle_id')
    # action_type = 1 收藏 0 取消收藏
    action_type = data.get('type')
    # 创建或获取UserCollectCircle对象
    user_collect_circle, created = UserCollectCircle.objects.get_or_create(user=user, circle_id=circle_id)
    # 更新收藏状态
    if action_type == '0':
        user_collect_circle.delete()
    else:
        user_collect_circle.save()
    # 更新圈子收藏数
    circle = Circle.objects.get(id=circle_id)
    circle.collect_number = circle.collect_number + 1 if action_type == '1' else circle.collect_number - 1
    circle.save()
    return result({})

"""用户关注（用户、圈子）"""
# 用户关注用户
@csrf_exempt
@jwt_required
def action_follow_user(request):
    user = CustomUser.objects.get(id=request.user_id)
    data = json.loads(request.body)
    user_id = data.get('user_id')
    # action_type = 1 关注 0 取消关注
    action_type = data.get('type')
    # 创建或获取UserFollowUser对象
    user_follow_user, created = UserFollowUser.objects.get_or_create(follower=user, following_id=user_id)
    # 更新关注状态
    if action_type == '0':
        user_follow_user.delete()
    else:
        user_follow_user.save()
    # 更新用户关注数
    user = CustomUser.objects.get(id=user_id)
    user.fan_number = user.fan_number + 1 if action_type == '1' else user.fan_number - 1
    user.save()
    return result({})

# 用户关注圈子
@csrf_exempt
@jwt_required
def action_follow_circle(request):
    user = CustomUser.objects.get(id=request.user_id)
    data = json.loads(request.body)
    circle_id = data.get('circle_id')
    # action_type = 1 关注 0 取消关注
    action_type = data.get('type')
    # 创建或获取UserFollowCircle对象
    user_follow_circle, created = UserFollowCircle.objects.get_or_create(follower=user, following_id=circle_id)
    # 更新关注状态
    if action_type == '0':
        user_follow_circle.delete()
    else:
        user_follow_circle.save()
    # 更新圈子关注数
    circle = Circle.objects.get(id=circle_id)
    circle.fan_number = circle.fan_number + 1 if action_type == '1' else circle.fan_number - 1
    circle.save()
    return result({})

"""用户举报（帖子、圈子、评论、用户）"""
# 用户举报帖子
def action_informant_post(request):
    pass

# 用户举报圈子
def action_informant_circle(request):
    pass

# 用户举报评论
def action_informant_comment(request):
    pass

# 用户举报用户
def action_informant_user(request):
    pass

"""消息通知"""
# 评论通知
def notify_comment_info(request):
    pass

# 回复通知
def notify_reply_info(request):
    pass

# 点赞通知
def notify_like_info(request):
    pass

# 关注通知
def notify_follow_info(request):
    pass
