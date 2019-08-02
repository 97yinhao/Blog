from django.http import JsonResponse
from users.models import UserProfile
import redis


def test_api(request):
    # JsonResponse 1、将返回内容序列化成json
    # 2、response中添加 content-type：application/json
    # return JsonResponse({"code": 200})
    pool = redis.ConnectionPool(
        host='localhost',
        port=6379,
        db=0,
        password='123456')
    r = redis.Redis(connection_pool=pool)
    # 加入redis分布式锁
    # set key value nx
    try:
        with r.lock('yh', blocking_timeout=3) as lock:
            u = UserProfile.objects.get(username='yh')
            u.score += 1
            u.save()
    except Exception as e:
        print('lock is failed')

    return JsonResponse({'msg': 'test is ok!'})
