import collections
import inspect
from django.shortcuts import render
from annoying.functions import get_object_or_None
from django.http import HttpResponse
from rest_framework.views import APIView
from django.utils.decorators import method_decorator
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

def lineno():
    """Returns the current line number in our program."""
    return inspect.currentframe().f_back.f_lineno

class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

def JSONError(message=None, code=404):
    stat = status.HTTP_404_NOT_FOUND
    if (code == 404):
        stat =status.HTTP_404_NOT_FOUND
    elif (code == 400):
        stat =status.HTTP_400_BAD_REQUEST
    elif (code == 500):
        stat =status.HTTP_500_BAD_REQUEST
    else:
        code=404
        stat = status.HTTP_404_NOT_FOUND

    error_msg = { "error": {"code": code, "message": message} }
    error_data = collections.OrderedDict(error_msg)
    return JSONResponse(error_data, status=stat)

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

class UserLikeList(APIView):
    """
    List all UserLikes, or create a new UserLike.
    """
    def get(self, request, format=None):
        username_list = request.GET.getlist('user')
        user_likes = None
        user_likes_serializer = None
        if (len(username_list) == 0):
            try:
                user_likes = UserLike.objects.all()
                user_likes_serializer = UserLikeSerializerGet(user_likes,
                                                              many=True)
                return JSONResponse(user_likes_serializer.data)
            except Exception as e:
                print(e)
                print("Line No: {0}".format(lineno()))
                return JSONError(message="UserLike is not found",
                                 code=404)

        user = None
        #User = get_user_model()
        try:
            user = int(username_list[0])
            user = get_object_or_None(authUser, id=user)
        except ValueError:
            user = get_object_or_None(authUser, username=username_list[0])
        if user is None:
            print("Line No: {0}".format(lineno()))
            return JSONError(message="User ID not Found", code=404)

        try:
            user_likes = UserLike.objects.filter(user=user.id)
        except UserLike.DoesNotExist:
            print("Line No: {0}".format(lineno()))
            return JSONError(message=
                             "User is not found in the Likes table",
                             code=404)
        if not user_likes.exists():
            print("Line No: {0}".format(lineno()))
            return JSONError(message=
                             "User is not found in the Likes table",
                             code=404)

        likes_serializer = UserLikeSerializerGet(user_likes, many=True)
        if likes_serializer:
            return JSONResponse(likes_serializer.data)
        else:
            print("Line No: {0}".format(lineno()))
            return JSONError(message= "UserLikes not Found", code=500)

    def post(self, request, format=None):
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
                print("Line No: {0}".format(lineno()))
                return JSONError(message="User is not found", code=404)
            user_like = get_object_or_None(UserLike, user=user_like_data["user"])
            if (user_like is not None):
                print("Line No: {0}".format(lineno()))
                return JSONError(message="Object is already created for the user",
                                 code=404)

            user_like_serializer = UserLikeSerializerPost(data=user_like_data)
            if user_like_serializer.is_valid():
                user_like_serializer.save()
                return JSONResponse(user_like_serializer.data,
                                    status=status.HTTP_201_CREATED)
            else:
                print("Line No: {0}".format(lineno()))
                return JSONError(message="Request data is not valid", code=400)
        except ValueError as ve:
            print("Line No: {0}".format(lineno()))
            return JSONError(message="Request data is not valid", code=400)
        except Exception as e:
            print("Line No: {0}".format(lineno()))
            return JSONError(message="UserLike is not created", code=500)

class UserLikeDetail(APIView):
    """
    Retrieve, update or delete a UserLike instance.
    """
    def get_object(self, pk):
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
            return {"message":"User ID not found", "code":404}
        try:
            user_like = UserLike.objects.get(user=user_details)
        except UserLike.DoesNotExist:
            print("Line No: {0}".format(lineno()))
            return {"message":"User is not found in the user likes table",
                    "code":404}
        return user_like

    def get(self, request, pk, format=None):
        user_like = self.get_object(pk)
        if (type(user_like) is dict):
            print("Line No: {0}".format(lineno()))
            return JSONError(user_like["message"], user_like["code"])
        try:
            user_like_serializer = UserLikeSerializerGet(user_like, many=False)
            return JSONResponse(user_like_serializer.data)
        except Exception as e:
            print("Line No: {0}".format(lineno()))
            return JSONError("UserLike is not found", code=500)

    def put(self, request, pk, format=None):
        user_like = self.get_object(pk)
        if (type(user_like) is dict):
            print("Line No: {0}".format(lineno()))
            return JSONError(user_like["message"], user_like["code"])
        try:
            user_add = []
            user_rmv = []
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
        except ValueError as ve:
            print(ve)
            print("Line No: {0}".format(lineno()))
            return JSONError(message="Request data is not valid", code=400)
        except Exception as e:
            print(e)
            print("Line No: {0}".format(lineno()))
            return JSONError(message="UserLike is not updated", code=403)

    def delete(self, request, pk, format=None):
        user_like = self.get_object(pk)
        if (type(user_like) is dict):
            print("Line No: {0}".format(lineno()))
            return JSONError(user_like["message"], user_like["code"])
        else:
            try:
                user_like.delete()
                return HttpResponse(status=status.HTTP_204_NO_CONTENT)
            except:
                print("Line No: {0}".format(lineno()))
                return JSONError(message="UserLike is not deleted", code=403)
