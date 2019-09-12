import collections
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from annoying.functions import get_object_or_None
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework import status
from users.models import User as authUser
from users.serializers import UserSerializer


class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

def JSONError(message=None, code=404, status=status.HTTP_404_NOT_FOUND):
    error_msg = { "error": {"code": code, "message": message} }
    error_data = collections.OrderedDict(error_msg)
    return JSONResponse(error_data, status=status)


@csrf_exempt
@api_view(['GET', 'POST'])
def user_list(request):
    if request.method == 'GET':
        username = request.GET.getlist('user')
        users = None
        users_serializer = None
        if (len(username) > 0):
            #User = get_user_model()
            try:
                user_a = int(username[0])
                users = get_object_or_None(authUser, id=user_a)
            except ValueError:
                users = get_object_or_None(authUser, username=username[0])
            if users is None:
                return JSONError(message=
                                 "User is not found in the User table",
                                 code=404)

            users_serializer = UserSerializer(users, many=False)
            return JSONResponse(users_serializer.data)

        else:
            users = authUser.objects.all()
            users_serializer = UserSerializer(users, many=True)
            return JSONResponse(users_serializer.data)
    elif request.method == 'POST':
        user_data = JSONParser().parse(request)
        if ('username' not in user_data):
            return JSONError(message="'username' required in the request data",
                             code=400, status=status.HTTP_400_BAD_REQUEST)

        user_serializer = UserSerializer(data=user_data)
        if user_serializer.is_valid():
            user_serializer.save()
            return JSONResponse(user_serializer.data,
                                status=status.HTTP_201_CREATED)
        return JSONResponse(user_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
def user_detail(request, pk):
    try:
        usr_id = int(pk)
        user = get_object_or_None(authUser, id=usr_id)
    except ValueError:
        user = get_object_or_None(authUser, username=pk)
    if user is None:
        return JSONError(message="User is not found",
                         code=404, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        user_serializer = UserSerializer(user)
        return JSONResponse(user_serializer.data)
    elif request.method == 'PUT':
        user_data = JSONParser().parse(request)
        if ('username' in user_data):
            if not isinstance(user_data['username'], (str, unicode)):
                return JSONError(message="'username' value is not a String",
                                 code=400, status=status.HTTP_400_BAD_REQUEST)

        user_serializer = UserSerializer(user, data=user_data)
        if user_serializer.is_valid():
            user_serializer.save()
            return JSONResponse(user_serializer.data)
        return JSONResponse(user_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        user.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)
