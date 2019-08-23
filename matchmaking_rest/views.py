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


v0 = [
    "questions",
    "answers",
    "questions-answers",
    "user-answers",
    "matches",
    "user-likes",
    "users",
]

v1 = []

@csrf_exempt
def api_root_list(request):
    if request.method == 'GET':
        return JSONResponse({"match-api": {
            "v0": v0,
            "v1": v1
        }})

@csrf_exempt
def api_match_list(request):
    if request.method == 'GET':
        return JSONResponse({
            "v0": v0,
            "v1": v1
        })

def api_v0_list(request):
    if request.method == 'GET':
        return JSONResponse(v0)
