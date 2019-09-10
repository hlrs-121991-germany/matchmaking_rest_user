import collections
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.decorators import api_view
from questions.models import Question
from questions.models import Answer
from questions.models import UserAnswer
#from django.contrib.auth.models import User as authUser
from users.models import User as authUser
#from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from annoying.functions import get_object_or_None
from questions.serializers import (QuestionSerializer, AnswerSerializer,
                                   QuestionSerializerPost,
                                   QuestionSerializerPut,
                                   UserAnswerSerializerGet,
                                   UserAnswerSerializerPost)

def JSONError(message=None, code=404, status=status.HTTP_404_NOT_FOUND):
    error_msg = { "error": {"code": code, "message": message} }
    error_data = collections.OrderedDict(error_msg)
    return JSONResponse(error_data, status=status)

class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


@csrf_exempt
@api_view(['GET', 'POST'])
def question_list(request):
    if request.method == 'GET':
        questions = Question.objects.all()
        questions_serializer = QuestionSerializer(questions, many=True)
        return JSONResponse(questions_serializer.data)
    elif request.method == 'POST':
        question_data = JSONParser().parse(request)
        if ('text' not in question_data):
            return JSONError(message="'text' is not found in request data",
                         code=400, status=status.HTTP_400_BAD_REQUEST)
        if ('answers' not in question_data):
            return JSONError(message="'answers' is not found in request data",
                         code=400, status=status.HTTP_400_BAD_REQUEST)
        question_serializer = QuestionSerializerPost(data=question_data)
        if question_serializer.is_valid():
            question_serializer.save()
            return JSONResponse(question_serializer.data,
                                status=status.HTTP_201_CREATED)
        return JSONResponse(question_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
def question_detail(request, pk):
    try:
        question_id = int(pk)
        question = get_object_or_None(Question, id=question_id)
    except ValueError:
        return JSONError(message="Question ID value is not an Integer",
                         code=400, status=status.HTTP_400_BAD_REQUEST)
    if question is None:
        return JSONError(message="Question is not found",
                         code=404, status=status.HTTP_404_NOT_FOUND)
    print(question.text)
    if request.method == 'GET':
        question_serializer = QuestionSerializer(question)
        return JSONResponse(question_serializer.data)
    elif request.method == 'PUT':
        ans_add = []
        ans_rmv = []
        try:
            answer_data = JSONParser().parse(request)
            if (("ans-add" not in answer_data) and
                    ("ans-remove" not in answer_data)):
                raise ValueError('Required key is not found in request data')
            if ("ans-add" in answer_data):
                if ((not isinstance(answer_data["ans-add"], (str, unicode))) or
                        (not (all(isinstance(int(x), int) for x in
                                 answer_data["ans-add"].split(","))))):
                    raise ValueError('Value is wrong in the "ans-add" data')
                else:
                    ans_add = answer_data["ans-add"].split(",")
            if ("ans-remove" in answer_data):
                if ((not isinstance(answer_data["ans-remove"],
                                    (str, unicode))) or
                        (not all(isinstance(int(x), int) for x in
                                 answer_data["ans-remove"].split(",")))):
                    raise ValueError('Value is wrong in the "ans-remove" data')
                else:
                    ans_rmv = answer_data["ans-remove"].split(",")
            if ("text" in answer_data):
                if (not isinstance(answer_data["text"],
                                    (str, unicode))):
                    raise ValueError('Value is wrong in the "text" data')
                else:
                    question.text = answer_data["text"]


            for ans_r in ans_rmv:
                answer_remove = get_object_or_None(Answer, pk=ans_r)
                if answer_remove is None:
                    raise ValueError("{0} is not valid in 'ans-remove'".format(ans_r))
            for ans_a in ans_add:
                answer_add = get_object_or_None(Answer, pk=ans_a)
                if answer_add is None:
                    raise ValueError("{0} is not valid in 'ans-add'".format(user_a))

            for ans_r in ans_rmv:
                answer_remove = Answer.objects.get(pk=ans_r)
                question.answers.remove(answer_remove)
            for ans_a in ans_add:
                answer_add = Answer.objects.get(pk=ans_a)
                question.answers.add(answer_add)
            question.save()

            question_serializer = QuestionSerializer(question, many=False)
            return JSONResponse(question_serializer.data)
        except ValueError, ve:
            print(ve)
            return JSONError(message=str(ve),
                             code=400, status=status.HTTP_400_BAD_REQUEST)
        except Exception, e:
            print(e)
            return JSONError(message="Object is not updated",
                             code=403, status=status.HTTP_403_FORBIDDEN)

        question_data = JSONParser().parse(request)
        question_serializer = QuestionSerializerPost(question, data=question_data)
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
@api_view(['GET', 'POST'])
def answer_list(request):
    if request.method == 'GET':
        answers = Answer.objects.all()
        answers_serializer = AnswerSerializer(answers, many=True)
        return JSONResponse(answers_serializer.data)
    elif request.method == 'POST':
        answer_data = JSONParser().parse(request)
        if ('text' not in answer_data):
            return JSONError(message="'text' is not found in request data",
                         code=400, status=status.HTTP_400_BAD_REQUEST)
        else:
            if (not isinstance(answer_data["text"], (str, unicode))):
                return JSONError(message="'text' value is not string",
                                 code=400, status=status.HTTP_400_BAD_REQUEST)

        answer_serializer = AnswerSerializer(data=answer_data)
        if answer_serializer.is_valid():
            answer_serializer.save()
            return JSONResponse(answer_serializer.data,
                                status=status.HTTP_201_CREATED)
        return JSONResponse(answer_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
def answer_detail(request, pk):
    try:
        answer_id = int(pk)
        answer = get_object_or_None(Answer, id=answer_id)
    except ValueError:
        return JSONError(message="Answer ID value is not an Integer",
                         code=400, status=status.HTTP_400_BAD_REQUEST)
    if answer is None:
        return JSONError(message="Answer is not found",
                         code=404, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        answer_serializer = AnswerSerializer(answer)
        return JSONResponse(answer_serializer.data)
    elif request.method == 'PUT':
        answer_data = JSONParser().parse(request)
        if ('text' not in answer_data):
            return JSONError(message="'text' is not found in request data",
                         code=400, status=status.HTTP_400_BAD_REQUEST)
        else:
            if (not isinstance(answer_data["text"], (str, unicode))):
                return JSONError(message="'text' value is not string",
                                 code=400, status=status.HTTP_400_BAD_REQUEST)
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
@api_view(['GET', 'POST'])
def user_answer_list(request):
    if request.method == 'GET':
        username_list = request.GET.getlist('user')
        print(username_list)
        user_answers = None
        if (len(username_list) == 0):
            user_answers = UserAnswer.objects.all()
        else:
            try:
                user_id = int(username_list[0])
                user_answers = UserAnswer.objects.filter(user=user_id)
                if not user_answers.exists():
                    return JSONError(message= "User ID not Found", code=404)
            except ValueError:
                #User = get_user_model()
                user = get_object_or_None(authUser, username=username_list[0])
                if user is None:
                    return JSONError(message= "User ID not Found", code=404)
                user_answers = UserAnswer.objects.filter(user=user.id)
            except UserAnswer.DoesNotExist:
                return JSONError(message= "User ID not Found", code=404)
        user_answers_serializer = UserAnswerSerializerGet(user_answers, many=True)
        print(user_answers, user_answers_serializer.data)
        return JSONResponse(user_answers_serializer.data)
    elif request.method == 'POST':
        user_answer_data = JSONParser().parse(request)
        if ('user' not in user_answer_data):
            return JSONError(message="'user' key is not found in request data",
                         code=400, status=status.HTTP_400_BAD_REQUEST)
        else:
            if not isinstance(user_answer_data['user'], int):
                return JSONError(message="'user' value is not an Integer",
                                 code=400, status=status.HTTP_400_BAD_REQUEST)
            else:
                #User = get_user_model()
                user_obj = get_object_or_None(authUser, id=int(user_answer_data['user']))
                if user_obj is None:
                    return JSONError(message="'user' object is not found",
                                     code=400, status=status.HTTP_400_BAD_REQUEST)
        if ('question' not in user_answer_data):
            return JSONError(message="'question' is not found in request data",
                         code=400, status=status.HTTP_400_BAD_REQUEST)
        else:
            if not isinstance(user_answer_data['question'], int):
                return JSONError(message="'question' value is not an Integer",
                                 code=400, status=status.HTTP_400_BAD_REQUEST)
            else:
                user_obj = get_object_or_None(Question, id=int(user_answer_data['question']))
                if user_obj is None:
                    return JSONError(message="'question' object is not found",
                                     code=400, status=status.HTTP_400_BAD_REQUEST)

        if ('my_answer' not in user_answer_data):
            return JSONError(message="'my_answer' is not found in request data",
                         code=400, status=status.HTTP_400_BAD_REQUEST)
        else:
            if not isinstance(user_answer_data['my_answer'], int):
                return JSONError(message="'my_answer' value is not an Integer",
                                 code=400, status=status.HTTP_400_BAD_REQUEST)
            else:
                user_obj = get_object_or_None(Answer, id=int(user_answer_data['my_answer']))
                if user_obj is None:
                    return JSONError(message="'my_answer' object is not found",
                                     code=400, status=status.HTTP_400_BAD_REQUEST)

        if ('my_answer_importance' not in user_answer_data):
            return JSONError(message="'my_answer_importance' is an not found in request data",
                         code=400, status=status.HTTP_400_BAD_REQUEST)
        else:
            if not isinstance(user_answer_data['my_answer_importance'], (str, unicode)):
                return JSONError(message="'my_answer_importance' value is not String",
                                 code=400, status=status.HTTP_400_BAD_REQUEST)

        if ('their_answer' not in user_answer_data):
            return JSONError(message="'their_answer' is not found in request data",
                         code=400, status=status.HTTP_400_BAD_REQUEST)
        else:
            if not isinstance(user_answer_data['their_answer'], int):
                return JSONError(message="'their_answer' value is not an Integer",
                                 code=400, status=status.HTTP_400_BAD_REQUEST)
            else:
                user_obj = get_object_or_None(Answer, id=int(user_answer_data['their_answer']))
                if user_obj is None:
                    return JSONError(message="'their_answer' object is not found",
                                     code=400, status=status.HTTP_400_BAD_REQUEST)

        if ('their_importance' not in user_answer_data):
            return JSONError(message="'their_importance' is not found in request data",
                         code=400, status=status.HTTP_400_BAD_REQUEST)
        else:
            if not isinstance(user_answer_data['their_importance'], (str, unicode)):
                return JSONError(message="'their_importance' value is not String",
                                 code=400, status=status.HTTP_400_BAD_REQUEST)

        user_answer_serializer = UserAnswerSerializerPost(data=user_answer_data)
        if user_answer_serializer.is_valid():
            user_answer_serializer.save()
            return JSONResponse(user_answer_serializer.data,
                                status=status.HTTP_201_CREATED)
        return JSONResponse(user_answer_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
def user_answer_detail(request, pk):
    try:
        usr_ans_id = int(pk)
        user_answer = get_object_or_None(UserAnswer, id=usr_ans_id)
    except ValueError:
        return JSONError(message="UserAnswer ID value is not an Integer",
                         code=400, status=status.HTTP_400_BAD_REQUEST)
    if user_answer is None:
        return JSONError(message="UserAnswer is not found",
                         code=404, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        user_answer_serializer = UserAnswerSerializerGet(user_answer)
        return JSONResponse(user_answer_serializer.data)
    elif request.method == 'PUT':
        user_answer_data = JSONParser().parse(request)
        if ('user' in user_answer_data):
            if not isinstance(user_answer_data['user'], int):
                return JSONError(message="'user' value is not an Integer",
                                 code=400, status=status.HTTP_400_BAD_REQUEST)
            else:
                #User = get_user_model()
                user_obj = get_object_or_None(authUser, id=int(user_answer_data['user']))
                if user_obj is None:
                    return JSONError(message="'user' object is not found",
                                     code=400, status=status.HTTP_400_BAD_REQUEST)
        if ('question' in user_answer_data):
            if not isinstance(user_answer_data['question'], int):
                return JSONError(message="'question' value is not an Integer",
                                 code=400, status=status.HTTP_400_BAD_REQUEST)
            else:
                user_obj = get_object_or_None(Question, id=int(user_answer_data['question']))
                if user_obj is None:
                    return JSONError(message="'question' object is not found",
                                     code=400, status=status.HTTP_400_BAD_REQUEST)

        if ('my_answer' in user_answer_data):
            if not isinstance(user_answer_data['my_answer'], int):
                return JSONError(message="'my_answer' value is not an Integer",
                                 code=400, status=status.HTTP_400_BAD_REQUEST)
            else:
                user_obj = get_object_or_None(Answer, id=int(user_answer_data['my_answer']))
                if user_obj is None:
                    return JSONError(message="'my_answer' object is not found",
                                     code=400, status=status.HTTP_400_BAD_REQUEST)

        if ('my_answer_importance' in user_answer_data):
            if not isinstance(user_answer_data['my_answer_importance'], (str, unicode)):
                return JSONError(message="'my_answer_importance' value is not String",
                                 code=400, status=status.HTTP_400_BAD_REQUEST)

        if ('their_answer' in user_answer_data):
            if not isinstance(user_answer_data['their_answer'], int):
                return JSONError(message="'their_answer' value is not an Integer",
                                 code=400, status=status.HTTP_400_BAD_REQUEST)
            else:
                user_obj = get_object_or_None(Answer, id=int(user_answer_data['their_answer']))
                if user_obj is None:
                    return JSONError(message="'their_answer' object is not found",
                                     code=400, status=status.HTTP_400_BAD_REQUEST)

        if ('their_importance' in user_answer_data):
            if not isinstance(user_answer_data['their_importance'], (str, unicode)):
                return JSONError(message="'their_importance' value is not String",
                                 code=400, status=status.HTTP_400_BAD_REQUEST)

        user_answer_serializer = UserAnswerSerializerPost(user_answer,
                                                      data=user_answer_data,
                                                          partial=True)
        if user_answer_serializer.is_valid():
            user_answer_serializer.save()
            return JSONResponse(user_answer_serializer.data)
        return JSONResponse(user_answer_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        user_answer.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)
