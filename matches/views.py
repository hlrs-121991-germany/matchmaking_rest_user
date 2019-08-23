from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework import status
from matches.models import Match
from matches.models import PositionMatch
from matches.models import EmployerMatch
from matches.models import LocationMatch
from matches.serializers import MatchSerializer
from matches.serializers import PositionMatchSerializer
from matches.serializers import EmployerMatchSerializer
from matches.serializers import LocationMatchSerializer


class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


@csrf_exempt
def match_list(request):
    if request.method == 'GET':
        Match.objects.update_all()
        matches = Match.objects.all()
        matches_serializer = MatchSerializer(matches, many=True)
        return JSONResponse(matches_serializer.data)
    elif request.method == 'POST':
        match_data = JSONParser().parse(request)
        match_serializer = MatchSerializer(data=match_data)
        if match_serializer.is_valid():
            match_serializer.save()
            Match.objects.update_all()
            return JSONResponse(match_serializer.data,
                                status=status.HTTP_201_CREATED)
        return JSONResponse(match_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
def match_detail(request, pk):
    try:
        Match.objects.update_all()
        match = Match.objects.get(pk=pk)
    except Match.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        match_serializer = MatchSerializer(match)
        return JSONResponse(match_serializer.data)
    elif request.method == 'PUT':
        match_data = JSONParser().parse(request)
        match_serializer = MatchSerializer(match, data=match_data)
        if match_serializer.is_valid():
            match_serializer.save()
            Match.objects.update_all()
            return JSONResponse(match_serializer.data)
        return JSONResponse(match_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        match.delete()
        Match.objects.update_all()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)


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


