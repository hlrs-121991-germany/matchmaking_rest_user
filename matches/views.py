import collections
import inspect
from django.shortcuts import render, get_object_or_404
from annoying.functions import get_object_or_None
#from django.contrib.auth import get_user_model
from django.http import HttpResponse
from rest_framework.views import APIView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework import status
from users.models import User as authUser
from matches.models import Match
from matches.models import PositionMatch
from matches.models import EmployerMatch
from matches.models import LocationMatch
from matches.serializers import MatchSerializer
from matches.serializers import PositionMatchSerializer
from matches.serializers import EmployerMatchSerializer
from matches.serializers import LocationMatchSerializer

match_update = False

import sys
if sys.version_info[0] >= 3:
    unicode = str

def lineno():
    """Returns the current line number in our program."""
    return inspect.currentframe().f_back.f_lineno

def JSONError(message=None, code=404):
    stat = status.HTTP_404_NOT_FOUND
    if (code == 404):
        stat = status.HTTP_404_NOT_FOUND
    elif (code == 400):
        stat = status.HTTP_400_BAD_REQUEST
    elif (code == 500):
        stat = status.HTTP_500_INTERNAL_SERVER_ERROR
    else:
        code=404
        stat = status.HTTP_404_NOT_FOUND

    error_msg = { "error": {"code": code, "message": message} }
    error_data = collections.OrderedDict(error_msg)
    return JSONResponse(error_data, status=stat)

class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


@method_decorator(csrf_exempt, name='dispatch')
class MatchList(APIView):
    def get(self, request, format=None):
        username_list = request.GET.getlist('user')
        matches = None
        matches_serializer = None
        global match_update

        if (match_update == True):
            Match.objects.update_all()
        else:
            match_update = True
            print("match_update is False")
            UserQuerySet = authUser.objects.all()
            for user_a in UserQuerySet:
                for user_b in UserQuerySet:
                    if (user_a == user_b):
                        continue

                    match_obj, match_stat = Match.objects.get_or_create_match(
                        user_a, user_b)
                    match_obj.do_match()
                    #if match_stat is True:
                    #    match_obj.do_match()
                    #    match_obj.save()
                    #else:
                    #    match_obj.do_match()

        if (len(username_list) == 2):
            user_a = None
            user_b = None
            #User = get_user_model()
            try:
                user_a = int(username_list[0])
                user_a = get_object_or_None(authUser, id=user_a)
            except ValueError:
                user_a = get_object_or_None(authUser, username=username_list[0])
            if user_a is None:
                return JSONError(message= "First User ID not Found", code=404)
            user_a=user_a.id

            try:
                user_b = int(username_list[1])
                user_b = get_object_or_None(authUser, id=user_b)
            except ValueError:
                user_b = get_object_or_None(authUser, username=username_list[1])
            if user_b is None:
                return JSONError(message= "Second User ID not Found", code=404)
            user_b=user_b.id

            if (user_a == user_b):
                return JSONError(message= "First & Second User ID are same", code=404)
            match_obj, match_stat = Match.objects.get_or_create_match(user_a,
                                                                      user_b)
            match_obj.do_match()
            #if match_stat is True:
            #    match_obj.do_match()
            #    match_obj.save()
            #else:
            #    match_obj.do_match()
            matches = match_obj
            matches_serializer = MatchSerializer(matches, many=False)
        elif (len(username_list) == 1):
            user_a = None
            #User = get_user_model()
            try:
                user_a = int(username_list[0])
                user_a = get_object_or_None(authUser, id=user_a)
            except ValueError:
                user_a = get_object_or_None(authUser, username=username_list[0])
            if user_a is None:
                return JSONError(message="User ID not Found", code=404)

            try:
                matches = Match.objects.filter(user_a=user_a.id)
                match_union = Match.objects.filter(user_b=user_a)
                matches = matches.union(match_union)
            except Match.DoesNotExist:
                return JSONError(message=
                                 "User is not found in the Matches table",
                                 code=404)

            if not matches.exists():
                return JSONError(message=
                                 "User is not found in the Matches table",
                                 code=404)

            for match_obj in matches:
                match_obj.do_match()

            try:
                matches = Match.objects.filter(user_a=user_a.id)
                match_union = Match.objects.filter(user_b=user_a)
                matches = matches.union(match_union)
            except Match.DoesNotExist:
                return JSONError(message=
                                 "User is not found in the Matches table",
                                 code=404)

            if not matches.exists():
                return JSONError(message=
                                 "User is not found in the Matches table",
                                 code=404)

            matches_serializer = MatchSerializer(matches, many=True)
#            user_a = get_object_or_404(User, username=username_list[0])
#            matches =  Match.objects.filter(user_a=user_a.id)
        else:
            matches = Match.objects.all()
            if not matches.exists():
                return JSONError(message= "User ID not Found", code=404)
            matches_serializer = MatchSerializer(matches, many=True)
        if matches_serializer:
            return JSONResponse(matches_serializer.data)
        else:
            return JSONError(message= "Matches not Found", code=404)

@method_decorator(csrf_exempt, name='dispatch')
class MatchDetail(APIView):
    """
    Retrieve, update or delete a Match instance.
    """
    def get_object(self, pk):
        try:
            #Match.objects.update_all()
            #match = Match.objects.get(pk=pk)
            match = get_object_or_None(Match, pk=pk)
            if match is None:
                message="Match is not found in the Matches table"
                return {"message": message, "code":404}
            else:
                match.do_match()
                match.save()
                return match
        except Match.DoesNotExist:
            message="Match is not found in the Matches table"
            return {"message": message, "code":500}

    def get(self, request, pk, format=None):
        match = self.get_object(pk)
        if (isinstance(match, dict) and
            ("message" in match) and ("code" in match) and
            (isinstance(match["message"], (str, unicode))) and
            (isinstance(match["code"], int))):
            print("Line No: {0}".format(lineno()))
            return JSONError(match["message"], match["code"])
        match_serializer = MatchSerializer(match)
        return JSONResponse(match_serializer.data)

@csrf_exempt
def position_match_list(request):
    if request.method == 'GET':
        position_matches = PositionMatch.objects.all()
        position_matches_serializer = PositionMatchSerializer(position_matches,
                                                              many=True)
        return JSONResponse(position_matches_serializer.data)
    elif request.method == 'POST':
        position_match_data = JSONParser().parse(request)
        position_match_serializer = PositionMatchSerializer(
            data = position_match_data)
        if position_match_serializer.is_valid():
            position_match_serializer.save()
            return JSONResponse(position_match_serializer.data,
                                status=status.HTTP_201_CREATED)
        return JSONResponse(position_match_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
def position_match_detail(request, pk):
    try:
        position_match = PositionMatch.objects.get(pk=pk)
    except PositionMatch.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        position_match_serializer = PositionMatchSerializer(position_match)
        return JSONResponse(position_match_serializer.data)
    elif request.method == 'PUT':
        position_match_data = JSONParser().parse(request)
        position_match_serializer = PositionMatchSerializer(
            position_match, data=position_match_data)
        if position_match_serializer.is_valid():
            position_match_serializer.save()
            return JSONResponse(position_match_serializer.data)
        return JSONResponse(position_match_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        position_match.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)

@csrf_exempt
def employer_match_list(request):
    if request.method == 'GET':
        employer_matches = EmployerMatch.objects.all()
        employer_matches_serializer = EmployerMatchSerializer(employer_matches, many=True)
        return JSONResponse(employer_matches_serializer.data)
    elif request.method == 'POST':
        employer_match_data = JSONParser().parse(request)
        employer_match_serializer = EmployerMatchSerializer(data=employer_match_data)
        if employer_match_serializer.is_valid():
            employer_match_serializer.save()
            return JSONResponse(employer_match_serializer.data,
                                status=status.HTTP_201_CREATED)
        return JSONResponse(employer_match_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
def employer_match_detail(request, pk):
    try:
        employer_match = EmployerMatch.objects.get(pk=pk)
    except EmployerMatch.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        employer_match_serializer = EmployerMatchSerializer(employer_match)
        return JSONResponse(employer_match_serializer.data)
    elif request.method == 'PUT':
        employer_match_data = JSONParser().parse(request)
        employer_match_serializer = EmployerMatchSerializer(employer_match, data=employer_match_data)
        if employer_match_serializer.is_valid():
            employer_match_serializer.save()
            return JSONResponse(employer_match_serializer.data)
        return JSONResponse(employer_match_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        employer_match.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)



@csrf_exempt
def location_match_list(request):
    if request.method == 'GET':
        location_matches = LocationMatch.objects.all()
        location_matches_serializer = LocationMatchSerializer(location_matches, many=True)
        return JSONResponse(location_matches_serializer.data)
    elif request.method == 'POST':
        location_match_data = JSONParser().parse(request)
        location_match_serializer = LocationMatchSerializer(data=location_match_data)
        if location_match_serializer.is_valid():
            location_match_serializer.save()
            return JSONResponse(location_match_serializer.data,
                                status=status.HTTP_201_CREATED)
        return JSONResponse(location_match_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
def location_match_detail(request, pk):
    try:
        location_match = LocationMatch.objects.get(pk=pk)
    except LocationMatch.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        location_match_serializer = LocationMatchSerializer(location_match)
        return JSONResponse(location_match_serializer.data)
    elif request.method == 'PUT':
        location_match_data = JSONParser().parse(request)
        location_match_serializer = LocationMatchSerializer(location_match, data=location_match_data)
        if location_match_serializer.is_valid():
            location_match_serializer.save()
            return JSONResponse(location_match_serializer.data)
        return JSONResponse(location_match_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        location_match.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)


