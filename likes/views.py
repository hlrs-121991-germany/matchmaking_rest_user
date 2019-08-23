from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
#from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from likes.models import UserLike
from likes.serializers import UserLikeSerializer
from likes.serializers import CurrentUserSerializer


class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

#       print(user_likes_serializer.data)
#        print(type(user_likes_serializer.data))
#        user_json = user_likes_serializer.data['user']
#        liked_users_json = user_likes_serializer.data['liked_users']
#        users = User.objects.all()
#        user_name = ""
#        liked_users_name = []
#        for user in users:
#            if (user.id == user_json):
#                user_name = user.username
#            elif ():
#                liked_users_name.append(user.username)
#        user_likes_json = { "user": user_name, "liked_users": liked_users_name}

@csrf_exempt
def user_like_list(request):
    if request.method == 'GET':
        print(request.data)
        user_likes = UserLike.objects.all()
        for user_like in user_likes:
            print(user_like.user, user_like.liked_users)
        user_likes = UserLike.objects.all()
        user_likes_serializer = UserLikeSerializer(user_likes, many=True)
        print(type(user_likes_serializer.data))
        return JSONResponse(user_likes_serializer.data)
    elif request.method == 'POST':
        user_like_data = JSONParser().parse(request)
        like_data = {"user": user_like_data[u'user'],                   \
                     "liked_users": user_like_data[u'liked_users']}
        print(user_like_data, like_data)
        user_like_serializer = UserLikeSerializer(data=user_like_data)
        print(user_like_serializer)
        like_serializer = UserLikeSerializer(data=like_data)
        print(like_serializer)
        print(like_serializer.is_valid())
        if user_like_serializer.is_valid():
            user_like_serializer.save()
            return JSONResponse(user_like_serializer.data,
                                status=status.HTTP_201_CREATED)
        return JSONResponse(user_like_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
def user_like_detail(request, pk):
    try:
        user_like = UserLike.objects.get(user=pk)
    except UserLike.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        user_like_serializer = UserLikeSerializer(user_like)
        return JSONResponse(user_like_serializer.data)
    elif request.method == 'PUT':
        user_like_data = JSONParser().parse(request)
        user_like_serializer = UserLikeSerializer(user_like,
                                                      data=user_like_data)
        if user_like_serializer.is_valid():
            user_like_serializer.save()
            return JSONResponse(user_like_serializer.data)
        return JSONResponse(user_like_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        user_like.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)
