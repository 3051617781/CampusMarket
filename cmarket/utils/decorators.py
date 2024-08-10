from functools import wraps  
from django.http import JsonResponse  
from utils.jwt import verify_jwt_token   
  
def jwt_required(view_func):  
    @wraps(view_func)  
    def wrapper(request, *args, **kwargs):  
        token = request.headers.get('Authorization')  # 假设JWT在Authorization头中，格式为"Bearer token" 
        if token:  
            _, token = token.split()  
            try:  
                user_id = verify_jwt_token(token)  
                # 可以将user_id附加到request对象上，以供后续使用  
                request.user_id = user_id  
            except Exception as e:  
                return JsonResponse({'error': str(e)}, status=401)  
        else:  
            return JsonResponse({'error': 'No token provided'}, status=401)  
        return view_func(request, *args, **kwargs)  
    return wrapper  