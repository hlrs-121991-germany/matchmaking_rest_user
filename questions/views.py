from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework import status
from questions.models import Question
from questions.models import Answer
from questions.models import UserAnswer
from questions.serializers import QuestionSerializer
from questions.serializers import AnswerSerializer
from questions.serializers import UserAnswerSerializer


class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


@csrf_exempt
def question_list(request):
    if request.method == 'GET':
        questions = Question.objects.all()
        questions_serializer = QuestionSerializer(questions, many=True)
        return JSONResponse(questions_serializer.data)
    elif request.method == 'POST':
        question_data = JSONParser().parse(request)
        question_serializer = QuestionSerializer(data=question_data)
        if question_serializer.is_valid():
            question_serializer.save()
            return JSONResponse(question_serializer.data,
                                status=status.HTTP_201_CREATED)
        return JSONResponse(question_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
def question_detail(request, pk):
    try:
        question = Question.objects.get(pk=pk)
    except Question.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        question_serializer = QuestionSerializer(question)
        return JSONResponse(question_serializer.data)
    elif request.method == 'PUT':
        question_data = JSONParser().parse(request)
        question_serializer = QuestionSerializer(question, data=question_data)
        if question_serializer.is_valid():
            question_serializer.save()
            return JSONResponse(question_serializer.data)
        return JSONResponse(question_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        question.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)

@csrf_exempt
def question_answer_list(request):
    if request.method == 'GET':
        questions = Question.objects.all()
        questions_serializer = QuestionSerializer(questions, many=True)
        answers = Answer.objects.all()
        answers_serializer = AnswerSerializer(answers, many=True)
        json_response = {
            'questions': questions_serializer.data,
            'answers': answers_serializer.data,
        }
        return JSONResponse(json_response)
    elif request.method == 'POST':
        question_data = JSONParser().parse(request)
        question_serializer = QuestionSerializer(data=question_data)
        if question_serializer.is_valid():
            question_serializer.save()
            return JSONResponse(question_serializer.data,
                                status=status.HTTP_201_CREATED)
        return JSONResponse(question_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
def question_answer_detail(request, pk):
    try:
        question = Question.objects.get(pk=pk)
    except Question.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        question_serializer = QuestionSerializer(question)
        return JSONResponse(question_serializer.data)
    elif request.method == 'PUT':
        question_data = JSONParser().parse(request)
        question_serializer = QuestionSerializer(question, data=question_data)
        if question_serializer.is_valid():
            question_serializer.save()
            return JSONResponse(question_serializer.data)
        return JSONResponse(question_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        question.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)



@csrf_exempt
def answer_list(request):
    if request.method == 'GET':
        answers = Answer.objects.all()
        answers_serializer = AnswerSerializer(answers, many=True)
        return JSONResponse(answers_serializer.data)
    elif request.method == 'POST':
        answer_data = JSONParser().parse(request)
        answer_serializer = AnswerSerializer(data=answer_data)
        if answer_serializer.is_valid():
            answer_serializer.save()
            return JSONResponse(answer_serializer.data,
                                status=status.HTTP_201_CREATED)
        return JSONResponse(answer_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
def answer_detail(request, pk):
    try:
        answer = Answer.objects.get(pk=pk)
    except Answer.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        answer_serializer = AnswerSerializer(answer)
        return JSONResponse(answer_serializer.data)
    elif request.method == 'PUT':
        answer_data = JSONParser().parse(request)
        answer_serializer = AnswerSerializer(answer, data=answer_data)
        if answer_serializer.is_valid():
            answer_serializer.save()
            return JSONResponse(answer_serializer.data)
        return JSONResponse(answer_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        answer.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)


@csrf_exempt
def user_answer_list(request):
    if request.method == 'GET':
        user_answers = UserAnswer.objects.all()
        user_answers_serializer = UserAnswerSerializer(user_answers, many=True)
        return JSONResponse(user_answers_serializer.data)
    elif request.method == 'POST':
        user_answer_data = JSONParser().parse(request)
        user_answer_serializer = UserAnswerSerializer(data=user_answer_data)
        if user_answer_serializer.is_valid():
            user_answer_serializer.save()
            return JSONResponse(user_answer_serializer.data,
                                status=status.HTTP_201_CREATED)
        return JSONResponse(user_answer_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
def user_answer_detail(request, pk):
    try:
        user_answer = UserAnswer.objects.get(pk=pk)
    except UserAnswer.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        user_answer_serializer = UserAnswerSerializer(answer)
        return JSONResponse(user_answer_serializer.data)
    elif request.method == 'PUT':
        user_answer_data = JSONParser().parse(request)
        user_answer_serializer = UserAnswerSerializer(user_answer,
                                                      data=user_answer_data)
        if user_answer_serializer.is_valid():
            user_answer_serializer.save()
            return JSONResponse(user_answer_serializer.data)
        return JSONResponse(user_answer_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        user_answer.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)
