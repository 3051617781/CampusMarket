# 返回前端模型封装
from .models import  CustomUser, School, SchoolRegion, Circle, Post, Comment
from typing import List, Dict, Any

# 用户
def res_user(user: CustomUser):
    return {
            'id': user.id,
            'nickname': user.nickname,
            'avator': user.avatar, 
            'signature': user.signature
        }

def res_user_list(users):
    return [res_user(user) for user in users]

def res_user_detail(user: CustomUser):
    return {
        "id": user.id,
        "nickname": user.nickname,
        "avator": user.avatar,
        "signature": user.signature,
        "gender": user.gender,
        "birthday": user.birthday,
        "school": user.school.name if user.school else None,
        "school_region": user.region.name if user.region else None,
        "school_id": user.school_id,
        "school_region_id": user.region_id,
        "hometown": user.hometown,
        "height": user.height
    }

# 圈子
def res_circle(circle: Circle):
    return {
        'id': circle.id,
        'name': circle.name,
        'avatar': circle.avatar,
        'description': circle.description,
        'created_at': circle.created_at,
        'like_number': circle.like_number,
        'collect_number': circle.collect_number,
        'fan_number': circle.fan_number
    }

def res_circle_list(circles):
    return [res_circle(circle) for circle in circles]

def res_circle_detail(circle: Circle):
    return {
        'id': circle.id,
        'name': circle.name,
        'avatar': circle.avatar,
        'description': circle.description,
        'created_at': circle.created_at,
        'like_number': circle.like_number,
        'collect_number': circle.collect_number,
        'fan_number': circle.fan_number
    }

# 帖子
def res_post(post: Post):
    image_urls = list(post.post_images.values_list('image__image', flat=True))
    circle = post.circle
    author = post.author
    
    return {
        'id': post.id,
        'author_nickname': author.nickname,
        'author_avator': author.avatar,
        'title': post.title,
        'content': post.content,
        'created_at': post.created_at,
        'post_images': image_urls, 
        'like_number': post.like_number,
        'collect_number': post.collect_number,
        'comment_number': post.comment_number,
        'circle_id': circle.id,
        'circle_avatar': circle.avatar,
        'circle_name': circle.name
    }

def res_post_list(posts):
    return [res_post(post) for post in posts]

def res_post_detail(post: Post):
    image_urls = list(post.post_images.values_list('image__image', flat=True))
    circle = post.circle
    author = post.author
    
    return {
        'id': post.id,
        'author_nickname': author.nickname,
        'author_avator': author.avatar,
        'title': post.title,
        'content': post.content,
        'created_at': post.created_at,
        'post_images': image_urls, 
        'like_number': post.like_number,
        'collect_number': post.collect_number,
        'comment_number': post.comment_number,
        'circle_id': circle.id,
        'circle_avatar': circle.avatar,
        'circle_name': circle.name
    }

# 评论
def res_comment(comment: Comment, subcomments: List['Comment'] = None) -> Dict[str, Any]:
    comment_data = {
        'id': comment.id,
        'user_id': comment.author.id,
        'user_avator': comment.author.avatar,
        'content': comment.content,
        'user_nickname': comment.author.nickname,
        'time': comment.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        'like_num': comment.like_number,
        'comment_num': comment.reply_number,
        'subcomment': res_subcomment_list(subcomments) if subcomments else []
    }
    return comment_data

def res_subcomment_list(subcomments: List[Comment]) -> List[Dict[str, Any]]:
    return [
        {
            'reply_id': subcomment.id,
            'id': subcomment.id,
            'user_id': subcomment.author.id,
            'user_avator': subcomment.author.avatar,
            'user_nickname': subcomment.author.nickname,
            'time': subcomment.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'like_num': subcomment.like_number,
            'comment_num': subcomment.reply_number
        }
        for subcomment in subcomments
    ]

def res_comment_list(comments: List[Comment]) -> List[Dict[str, Any]]:
    return [
        res_comment(comment, comment.replies.all()) for comment in comments
    ]