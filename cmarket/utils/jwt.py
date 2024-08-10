import jwt  
from datetime import datetime, timedelta  
from django.conf import settings  
from app.models import CustomUser

def generate_jwt_token(user):  
    payload = {  
        'user_id': user.id,  
        'exp': datetime.utcnow() + timedelta(days=1),  # 设置过期时间  
    }  
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')  
    # return token.decode('utf-8')  # string object has no attribute decode
    return token 
 
def verify_jwt_token(token):  
    try:  
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])  
        user_id = payload.get('user_id')  
        # 从数据库检索用户  
        CustomUser.objects.get(id=user_id)  
        # 可以在这里添加更复杂的验证逻辑，比如检查用户状态等  
        return user_id  
    except jwt.ExpiredSignatureError:  
        # 令牌已过期  
        raise Exception("Token is expired")  
    except jwt.DecodeError:  
        # 令牌无法解码  
        raise Exception("Token is invalid")  
    except User.DoesNotExist:  
        # 用户不存在  
        raise Exception("User not found")
    