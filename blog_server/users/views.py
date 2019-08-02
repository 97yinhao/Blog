from django.shortcuts import render
from django.http import JsonResponse
import json

from tools.logging_decorator import logging_check
from .models import UserProfile
import hashlib
import jwt
import time

# Create your views here.

@logging_check('PUT')
def users(request, username=None):
    if request.method == 'GET':
        # 取数据
        if username:
            # 具体用户数据
            # /v1/users/yh?info=1&email=1 {'info':xxx 'email':xxx}
            try:
                user = UserProfile.objects.get(username=username)
            except UserProfile.DoesNotExist:
                user = None
            if not user:
                # 用户不存在
                result = {'code': 208, 'error': 'The user is not existed'}
                return JsonResponse(result)
            # 判断查询字符串
            if request.GET.keys():
                # 证明有查询字符串
                data = {}
                for k in request.GET.keys():
                    # 数据库中最好有非空默认值
                    if hasattr(user, k):
                        data[k] = getattr(user, k)
                result = {'code': 200, 'username': username, 'data': data}
                return JsonResponse(result)
            else:
                # 证明指定查询用户全量数据
                result = {
                    'code': 200,
                    'username': username,
                    'data': {
                        'info': user.info,
                        'sign': user.sign,
                        'nickname': user.nickname,
                        'avatar': str(
                            user.avatar)}}
                return JsonResponse(result)
        else:
            # 全部用户的数据
            all_users = UserProfile.objects.all()
            res = []
            for u in all_users:
                d = {}
                d['username'] = u.username
                d['email'] = u.email
                res.append(d)
                # [{username:xxx,..}, {username:xx,..}]
            result = {'code': 200, 'data': res}
            return JsonResponse(result)

    elif request.method == 'POST':
        # 注册用户
        # 密码需用SHA-1 hashlib.sha1() -> update -> hexdigest()

        # 获取json数据
        json_str = request.body
        if not json_str:
            # 前端异常提交，空数据
            result = {'code': 202, 'error': 'Please POST data'}
            return JsonResponse(result)
        # 反序列化json str
        json_obj = json.loads(json_str)
        username = json_obj.get('username')
        email = json_obj.get('email')
        password_1 = json_obj.get('password_1')
        password_2 = json_obj.get('password_2')
        if not username:
            result = {'code': 203, 'error': 'Please give me username'}
            return JsonResponse(result)
        if not email:
            # email 不存在
            result = {'code': 204, 'error': 'Please give me email'}
            return JsonResponse(result)
        if not password_1 or not password_2:
            # p1 p2 不存在
            result = {'code': 205, 'error': 'Please give me password'}
            return JsonResponse(result)
        if password_1 != password_2:
            # p1 p2 不一致
            result = {'code': 206, 'error': 'The password is wrong !'}
            return JsonResponse(result)
        # 检查用户是否存在
        old_user = UserProfile.objects.filter(username=username)
        if old_user:
            # 该用户已经注册
            result = {'code': 207, 'error': 'The username is existed!'}
            return JsonResponse(result)
        # 将密码进行hash
        h_p = hashlib.sha1()
        h_p.update(password_1.encode())
        try:
            UserProfile.objects.create(
                username=username,
                nickname=username,
                email=email,
                password=h_p.hexdigest())
        except Exception as e:
            print('UserProfile create error is %s' % e)
            result = {'code': 207, 'error': 'The username is existed!'}
            return JsonResponse(result)
        # 根据用户名 生成token
        token = make_token(username)
        result = {
            'code': 200,
            'username': username,
            'data': {
                'token': token.decode()}}
        return JsonResponse(result)

    elif request.method == 'PUT':
        # 修改用户数据 /v1/users/用户名
        user = request.user
        json_str = request.body
        # 判断前端是否给了json串
        if not json_str:
            result = {'code': 202, 'error': 'Please give me data'}
            return JsonResponse(result)
        json_obj = json.loads(json_str)
        nickname = json_obj.get('nickname')
        # 昵称不能为空
        if not nickname:
            result = {'code': 209, 'error': 'Please give me nickname'}
            return JsonResponse(result)
        # sign&info 默认值为空字符串
        sign = json_obj.get('sign', '')
        info = json_obj.get('info', '')

        # 存
        user.sign = sign
        user.info = info
        user.nickname = nickname
        user.save()

        result = {'code': 200, 'username': username}
        return JsonResponse(result)

    return JsonResponse({'code': 200, 'data': {'username': 1}})


def make_token(username, expire=3600 * 24):
    """
    生成token
    :param username:
    :param expire:
    :return:
    """
    key = 'abcdef1234'
    now_t = time.time()
    payload = {'username': username, 'exp': int(now_t + expire)}
    return jwt.encode(payload, key, algorithm='HS256')


@logging_check('POST')
def user_avatar(request, username):
    # 上传图片思路：
    # 1，前端 -> form post 提交 并且 content-type要改成multipart/form-data
    # 2，后端只要拿到post提交，request.FILES['avatar']
    if not request.method == 'POST':
        result = {'code': 210, 'error': 'Please use POST'}
        return JsonResponse(result)

    user = request.user
    if not users:
        result = {'code': 208, 'error': 'The username is not existed !'}
        return JsonResponse(result)
    if request.FILES.get('avatar'):
        user.avatar = request.FILES['avatar']
        user.save()
        result = {'code': 200, 'username': username}
        return JsonResponse(result)
    else:
        result = {'code': 211, 'error': 'Please give me avatar'}
        return JsonResponse(result)