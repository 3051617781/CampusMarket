from django.http import JsonResponse
def result(data):
    return JsonResponse({
        "code": 200,
        "msg": "success",
        "data": data
    })

def err(code, msg):
    return JsonResponse({
        "code": code,
        "msg": msg
    })

