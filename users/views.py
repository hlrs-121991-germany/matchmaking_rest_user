import collections
import inspect
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from annoying.functions import get_object_or_None
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework import status
from users.models import User as authUser
from users.serializers import UserSerializer

def lineno():
    """Returns the current line number in our program."""
    return inspect.currentframe().f_back.f_lineno

class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

def JSONError(message=None, code=404):
    stat = None
    if (code == 400):
        stat = status.HTTP_400_BAD_REQUEST
    elif (code == 500):
        stat = status.HTTP_500_INTERNAL_SERVER_ERROR
    else:
        code = 404
        stat = status.HTTP_404_NOT_FOUND

    error_msg = { "error": {"code": code, "message": message} }
    error_data = collections.OrderedDict(error_msg)
    return JSONResponse(error_data, status=stat)


@method_decorator(csrf_exempt, name='dispatch')
class UserList(APIView):
    """
    List all Users, or create a new User.
    """
    def get(self, request, format=None):
        username = request.GET.getlist('user')
        users = None
        users_serializer = None
        if (len(username) > 0):
            #User = get_user_model()
            print(username)
            try:
                user_a = int(username[0])
                users = get_object_or_None(authUser, id=user_a)
            except ValueError:
                users = get_object_or_None(authUser, username=username[0])
            if users is None:
                return JSONError(message=
                                 "User is not found in the User table",
                                 code=404)

            try:
                users_serializer = UserSerializer(users, many=False)
                return JSONResponse(users_serializer.data)
            except Exception:
                print("Line No: {0}".format(lineno()))
                return JSONError(message="User is not found", code=500)

        else:
            try:
                users = authUser.objects.all()
                users_serializer = UserSerializer(users, many=True)
                return JSONResponse(users_serializer.data)
            except Exception:
                print("Line No: {0}".format(lineno()))
                return JSONError(message="User is not found", code=500)

    def post(self, request, format=None):
        try:
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
        except Exception:
            print("Line No: {0}".format(lineno()))
            return JSONError(message="User is not created", code=500)


@method_decorator(csrf_exempt, name='dispatch')
class UserDetail(APIView):
    """
    Retrieve, update or delete a Question instance.
    """
    def get_object(self, pk):
        try:
            usr_id = int(pk)
            user = get_object_or_None(authUser, id=usr_id)
        except ValueError:
            user = get_object_or_None(authUser, username=pk)
        if user is None:
            print("Line No: {0}".format(lineno()))
            return {"message": "User is not found", "code":404}
        else:
            return user

    def get(self, request, pk, format=None):
        try:
            user = self.get_object(pk)
            if (isinstance(user, dict) and
                ("message" in user) and ("code" in user) and
                (isinstance(user["message"], (str, unicode))) and
                (isinstance(user["code"], int))):
                print("Line No: {0}".format(lineno()))
                return JSONError(user["message"], user["code"])

            user_serializer = UserSerializer(user)
            return JSONResponse(user_serializer.data)
        except Exception as e:
            return JSONError("User is not found", 500)

    def put(self, request, pk, format=None):
        try:
            user = self.get_object(pk)
            if (isinstance(user, dict) and
                ("message" in user) and ("code" in user) and
                (isinstance(user["message"], (str, unicode))) and
                (isinstance(user["code"], int))):
                print("Line No: {0}".format(lineno()))
                return JSONError(user["message"], user["code"])

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
        except Exception as e:
            print(e)
            print("Line No: {0}".format(lineno()))
            return JSONError(message="User is not updated", code=500)

    def delete(self, request, pk, format=None):
        try:
            user = self.get_object(pk)
            if (isinstance(user, dict) and
                ("message" in user) and ("code" in user) and
                (isinstance(user["message"], (str, unicode))) and
                (isinstance(user["code"], int))):
                print("Line No: {0}".format(lineno()))
                return JSONError(user["message"], user["code"])

            user.delete()
            return HttpResponse(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            print(e)
            print("Line No: {0}".format(lineno()))
            return JSONError(message="User is not deleted", code=500)

