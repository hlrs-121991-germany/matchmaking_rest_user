import collections
from django.shortcuts import render
from annoying.functions import get_object_or_None
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
#from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view, schema, renderer_classes
#from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from likes.models import UserLike
from users.models import User as authUser
from rest_framework.schemas import AutoSchema
from rest_framework.serializers import Serializer
from rest_framework_swagger import renderers
from likes.serializers import (UserLikeSerializerGet, CurrentUserSerializer,
                               UserLikeSerializerPost, UserLikeSerializerGUI)


class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

def JSONError(message=None, code=404, status=status.HTTP_404_NOT_FOUND):
    error_msg = { "error": {"code": code, "message": message} }
    error_data = collections.OrderedDict(error_msg)
    return JSONResponse(error_data, status=status)

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

class CustomAutoSchema(AutoSchema):
    pass

@csrf_exempt
@api_view(['GET', 'POST'])
@schema(CustomAutoSchema())
@renderer_classes([renderers.OpenAPIRenderer, renderers.SwaggerUIRenderer])
def user_like_list(request):
    if request.method == 'GET':
        username_list = request.GET.getlist('user')
        user_likes = None
        user_likes_serializer = None
        if (len(username_list) == 0):
            user_likes = UserLike.objects.all()
            user_likes_serializer = UserLikeSerializerGet(user_likes, many=True)
            return JSONResponse(user_likes_serializer.data)

        user = None
        #User = get_user_model()
        try:
            user = int(username_list[0])
            user = get_object_or_None(authUser, id=user)
        except ValueError:
            user = get_object_or_None(authUser, username=username_list[0])
        if user is None:
            return JSONError(message="User ID not Found", code=404)

        try:
            user_likes = UserLike.objects.filter(user=user.id)
        except UserLike.DoesNotExist:
            return JSONError(message=
                             "User is not found in the Likes table",
                             code=404)
        if not user_likes.exists():
            return JSONError(message=
                             "User is not found in the Likes table",
                             code=404)

        likes_serializer = UserLikeSerializerGet(user_likes, many=True)
        if likes_serializer:
            return JSONResponse(likes_serializer.data)
        else:
            return JSONError(message= "Matches not Found", code=404)

    elif request.method == 'POST':
        try:
            user_like_data = JSONParser().parse(request)
            if (("user" not in user_like_data) or
                    ("liked_users" not in user_like_data) or
                    (not isinstance(user_like_data["user"], int)) or
                    (not isinstance(user_like_data["liked_users"], list)) or
                    (not all(isinstance(x, int) for x in
                             user_like_data["liked_users"]))):
                raise ValueError('Key: Value is wrong in the data')
            user = get_object_or_None(authUser, id=user_like_data["user"])
            if (user is None):
                return JSONError(message="User is not found",
                                 code=404)
            user_like = get_object_or_None(UserLike, user=user_like_data["user"])
            if (user_like is not None):
                return JSONError(message="Object is already created for the user",
                                 code=404)

            user_like_serializer = UserLikeSerializerPost(data=user_like_data)
            if user_like_serializer.is_valid():
                user_like_serializer.save()
                return JSONResponse(user_like_serializer.data,
                                    status=status.HTTP_201_CREATED)
            else:
                return JSONError(message="Request data is not valid",
                             code=400, status=status.HTTP_400_BAD_REQUEST)
        except ValueError, ve:
            return JSONError(message="Request data is not valid",
                             code=400, status=status.HTTP_400_BAD_REQUEST)
        except Exception, e:
            return JSONError(message="Object is already created for the user",
                             code=404)

user_like_list.get_serializer = lambda *args: UserLikeSerializerGUI

@csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
def user_like_detail(request, pk):
    user_like = None
    user_id = -1
    try:
        user_id = int(pk)
        #User = get_user_model()
        user_details = get_object_or_None(authUser, id=pk)
    except ValueError:
        #User = get_user_model()
        user_details = get_object_or_None(authUser, username=pk)
    if user_details is not None:
        user_id = user_details.id
    else:
        return JSONError(message="User ID not found",
                         code=404)
    print(user_id)
    try:
        user_like = UserLike.objects.get(user=user_details)
    except UserLike.DoesNotExist:
        return JSONError(message="User is not found in the likes table",
                         code=404)
    if request.method == 'GET':
        if user_like is not None:
            user_like_serializer = UserLikeSerializerGet(user_like, many=False)
            return JSONResponse(user_like_serializer.data)
        else:
            return JSONError(message="User ID not found",
                             code=404)
    elif request.method == 'PUT':
        user_add = []
        user_rmv = []
        if user_like is None:
            return JSONError(message="User ID not found",
                             code=404)
        try:
            user_like_data = JSONParser().parse(request)
            if (("add" not in user_like_data) and
                    ("remove" not in user_like_data)):
                raise ValueError('Required key is not found in request data')
            #User = get_user_model()
            if ("add" in user_like_data):
                if ((not isinstance(user_like_data["add"], (str, unicode))) or
                        (not (all(isinstance(int(x), int) for x in
                                 user_like_data["add"].split(","))))):
                    raise ValueError('Value is wrong in the "add" data')
                else:
                    user_add = user_like_data["add"].split(",")
            if ("remove" in user_like_data):
                if ((not isinstance(user_like_data["remove"],
                                    (str, unicode))) or
                        (not all(isinstance(int(x), int) for x in
                                 user_like_data["remove"].split(",")))):
                    raise ValueError('Value is wrong in the "remove" data')
                else:
                    user_rmv = user_like_data["remove"].split(",")


            for user_r in user_rmv:
                user_remove = get_object_or_None(authUser, pk=user_r)
                if user_remove is None:
                    raise ValueError("{0} is not valid in 'remove'".format(user_r))
            for user_a in user_add:
                user_adding = get_object_or_None(authUser, pk=user_a)
                if user_adding is None:
                    raise ValueError("{0} is not valid in 'add'".format(user_a))

            for user_r in user_rmv:
                user_remove = authUser.objects.get(id=user_r)
                user_like.liked_users.remove(user_remove)
            for user_a in user_add:
                user_adding = authUser.objects.get(id=user_a)
                user_like.liked_users.add(user_adding)
            user_like.save()

            user_like_serializer = UserLikeSerializerGet(user_like, many=False)
            return JSONResponse(user_like_serializer.data)
        except ValueError, ve:
            print(ve)
            return JSONError(message="Request data is not valid",
                             code=400, status=status.HTTP_400_BAD_REQUEST)
        except Exception, e:
            print(e)
            return JSONError(message="Object is not updated",
                             code=403, status=status.HTTP_403_FORBIDDEN)
    elif request.method == 'DELETE':
        if user_like is None:
            return JSONError(message="User ID not found",
                             code=404)
        else:
            try:
                user_like.delete()
                return HttpResponse(status=status.HTTP_204_NO_CONTENT)
            except:
                return JSONError(message="Object is not deleted",
                                 code=403, status=status.HTTP_403_FORBIDDEN)
