import datetime
import json

from django.shortcuts import render
from django.http import JsonResponse

from tools.logging_decorator import logging_check
from topic.models import Topic
from users.models import UserProfile
from .models import Message

# Create your views here.


@logging_check('POST')
def messages(request, topic_id):
    """
    留言/回复
    :param request:
    :param topic_id:
    :return:
    """
    if request.method == 'POST':
        # 创建　留言/回复
        user = request.user
        json_str = request.body
        if not json_str:
            result = {'code': 402, 'error': 'Please give me json str'}
            return JsonResponse(result)
        json_obj = json.loads(json_str)
        # 留言内容
        content = json_obj.get('content')
        # 父级留言的ID
        parent_id = json_obj.get('parent_id', 0)
        if not content:
            result = {'code': 403, 'error': 'Please give me content'}
            return JsonResponse(result)
        # 当前时间
        now = datetime.datetime.now()
        try:
            topic = Topic.objects.get(id=topic_id)
        except Exception as e:
            result = {'code': 404, 'error': 'This topic is not existed'}
            return JsonResponse(result)
        # 判断当前topic limit
        if topic.limit == 'private':
            # 如果当前limit是私有的,则必须为博主方可评论
            if user.username != topic.author.username:
                result = {'code': 405, 'error': 'Please go out!'}
                return JsonResponse(result)
        Message.objects.create(topic=topic, content=content, parent_message=parent_id, created_time=now, publisher=user)
        return JsonResponse({'code': 200, 'data': {}})

