from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from django.core.exceptions import ObjectDoesNotExist, ValidationError
"""=======异常处理======"""
class ExceptionMiddleware(MiddlewareMixin):
    def process_exception(self, request, exception):
        if isinstance(exception, ObjectDoesNotExist):
            return JsonResponse({'code': '404', 'msg': f'对象不存在'}, status=404)
        elif isinstance(exception, ValidationError):
            return JsonResponse({'code': '400', 'msg': str(exception)}, status=400)
        else:
            return JsonResponse({'code': '500', 'msg': '服务器错误'}, status=500)

    