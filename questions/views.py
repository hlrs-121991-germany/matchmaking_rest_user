import collections
import inspect
from django.shortcuts import render
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
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

import sys
if sys.version_info[0] >= 3:
    unicode = str

def lineno():
    """Returns the current line number in our program."""
    return inspect.currentframe().f_back.f_lineno


def JSONError(message=None, code=404):
    stat = status.HTTP_404_NOT_FOUND
    if (code == 404):
        stat =status.HTTP_404_NOT_FOUND
    elif (code == 400):
        stat =status.HTTP_400_BAD_REQUEST
    elif (code == 500):
        stat =status.HTTP_500_INTERNAL_SERVER_ERROR
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
class QuestionList(APIView):
    """
    List all Questions, or create a new Question.
    """
    def get(self, request, format=None):
        try:
            questions = Question.objects.all()
            questions_serializer = QuestionSerializer(questions, many=True)
            return JSONResponse(questions_serializer.data)
        except Exception as e:
            print(e)
            print("Line No: {0}".format(lineno()))
            return JSONError(message="Question List is not found", code=500)

    def post(self, request, format=None):
        try:
            question_data = JSONParser().parse(request)
            if (('text' not in question_data) or
                    (not isinstance(question_data["text"], (str, unicode)))):
                print("Line No: {0}".format(lineno()))
                return JSONError(message="'text' is not valid in request data",
                                 code=400)
            if (('answers' not in question_data) or
                    (not isinstance(question_data["answers"], list))):
                print("Line No: {0}".format(lineno()))
                return JSONError(message="'answers' is not valid in request data",
                                 code=400)
            question_serializer = QuestionSerializerPost(data=question_data)
            if question_serializer.is_valid():
                question_serializer.save()
                return JSONResponse(question_serializer.data,
                                    status=status.HTTP_201_CREATED)
            return JSONResponse(question_serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            print("Line No: {0}".format(lineno()))
            return JSONError(message="Question is not updated", code=500)

@method_decorator(csrf_exempt, name='dispatch')
class QuestionDetail(APIView):
    """
    Retrieve, update or delete a Question instance.
    """
    def get_object(self, pk):
        try:
            question_id = int(pk)
            question = get_object_or_None(Question, id=question_id)
        except ValueError as ve:
            print(ve)
            print("Line No: {0}".format(lineno()))
            return {"message":"Question ID value is not an Integer",
                    "code": 400}

        if question is None:
            return {"message":"Question is not found", "code":404}
        else:
            return question

    def get(self, request, pk, format=None):
        try:
            question = self.get_object(pk)
            if (isinstance(question, dict) and
                ("message" in question) and ("code" in question) and
                (isinstance(question["message"], (str, unicode))) and
                (isinstance(question["code"], int))):
                print("Line No: {0}".format(lineno()))
                return JSONError(question["message"], question["code"])

            question_serializer = QuestionSerializer(question)
            return JSONResponse(question_serializer.data)
        except Exception as e:
            return JSONError("Question is not found", 500)

    def put(self, request, pk, format=None):
        question = self.get_object(pk)
        if (isinstance(question, dict) and
            ("message" in question) and ("code" in question) and
            (isinstance(question["message"], (str, unicode))) and
            (isinstance(question["code"], int))):
            print("Line No: {0}".format(lineno()))
            return JSONError(question["message"], question["code"])

        try:
            answer_data = JSONParser().parse(request)
            ans_add = []
            ans_rmv = []
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
                    raise ValueError("{0} is not valid in 'ans-add'".format(ans_a))

            for ans_r in ans_rmv:
                answer_remove = Answer.objects.get(pk=ans_r)
                question.answers.remove(answer_remove)
            for ans_a in ans_add:
                answer_add = Answer.objects.get(pk=ans_a)
                question.answers.add(answer_add)
            question.save()

            question_serializer = QuestionSerializer(question, many=False)
            return JSONResponse(question_serializer.data)
        except ValueError as ve:
            print(ve)
            print("Line No: {0}".format(lineno()))
            return JSONError(message=str(ve), code=400)
        except Exception as e:
            print(e)
            print("Line No: {0}".format(lineno()))
            return JSONError(message="Object is not updated", code=500)

    def delete(self, request, pk, format=None):
        question = self.get_object(pk)
        if (isinstance(question, dict) and
            ("message" in question) and ("code" in question) and
            (isinstance(question["message"], (str, unicode))) and
            (isinstance(question["code"], int))):
            print("Line No: {0}".format(lineno()))
            return JSONError(question["message"], question["code"])

        try:
            question.delete()
            return HttpResponse(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            print(e)
            print("Line No: {0}".format(lineno()))
            return JSONError(message="Question is not deleted", code=500)


@method_decorator(csrf_exempt, name='dispatch')
class AnswerList(APIView):
    """
    List all Answers, or create a new Answer.
    """
    def get(self, request, format=None):
        try:
            answers = Answer.objects.all()
            answers_serializer = AnswerSerializer(answers, many=True)
            return JSONResponse(answers_serializer.data)
        except Exception as e:
            print(e)
            print("Line No: {0}".format(lineno()))
            return JSONError(message="Question List is not found", code=500)

    def post(self, request, format=None):
        try:
            answer_data = JSONParser().parse(request)
            if ('text' not in answer_data):
                print("Line No: {0}".format(lineno()))
                return JSONError(message="'text' is not found in request data",
                                 code=400)
            else:
                if (not isinstance(answer_data["text"], (str, unicode))):
                    print("Line No: {0}".format(lineno()))
                    return JSONError(message="'text' value is not string",
                                     code=400)

            answer_serializer = AnswerSerializer(data=answer_data)
            if answer_serializer.is_valid():
                answer_serializer.save()
                return JSONResponse(answer_serializer.data,
                                    status=status.HTTP_201_CREATED)
            return JSONResponse(answer_serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            print("Line No: {0}".format(lineno()))
            return JSONError(message="Answer is not updated", code=500)

@method_decorator(csrf_exempt, name='dispatch')
class AnswerDetail(APIView):
    """
    Retrieve, update or delete an Answer instance.
    """
    def get_object(self, pk):
        try:
            answer_id = int(pk)
            answer = get_object_or_None(Answer, id=answer_id)
        except ValueError as ve:
            print(ve)
            print("Line No: {0}".format(lineno()))
            return {"message":"Answer ID value is not an Integer",
                    "code":400}
        if answer is None:
            return {"message":"Answer is not found", "code":404}
        return answer


    def get(self, request, pk, format=None):
        answer = self.get_object(pk)
        if (isinstance(answer, dict) and
            ("message" in answer) and ("code" in answer) and
            (isinstance(answer["message"], (str, unicode))) and
            (isinstance(answer["code"], int))):
            print("Line No: {0}".format(lineno()))
            return JSONError(answer["message"], answer["code"])

        try:
            answer_serializer = AnswerSerializer(answer)
            return JSONResponse(answer_serializer.data)
        except Exception as e:
            print(e)
            print("Line No: {0}".format(lineno()))
            return JSONError(message="Answer is not found", code=500)

    def put(self, request, pk, format=None):
        answer = self.get_object(pk)
        if (isinstance(answer, dict) and
            ("message" in answer) and ("code" in answer) and
            (isinstance(answer["message"], (str, unicode))) and
            (isinstance(answer["code"], int))):
            print("Line No: {0}".format(lineno()))
            return JSONError(answer["message"], answer["code"])

        try:
            answer_data = JSONParser().parse(request)
            if ('text' not in answer_data):
                print("Line No: {0}".format(lineno()))
                return JSONError(message="'text' is not found in request data",
                                 code=400)
            else:
                if (not isinstance(answer_data["text"], (str, unicode))):
                    print("Line No: {0}".format(lineno()))
                    return JSONError(message="'text' value is not string",
                                     code=400)
            answer_serializer = AnswerSerializer(answer, data=answer_data)
            if answer_serializer.is_valid():
                answer_serializer.save()
                return JSONResponse(answer_serializer.data)
            return JSONResponse(answer_serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            print("Line No: {0}".format(lineno()))
            return JSONError(message="Answer is not updated", code=500)

    def delete(self, request, pk, format=None):
        answer = self.get_object(pk)
        if (isinstance(answer, dict) and
            ("message" in answer) and ("code" in answer) and
            (isinstance(answer["message"], (str, unicode))) and
            (isinstance(answer["code"], int))):
            print("Line No: {0}".format(lineno()))
            return JSONError(answer["message"], answer["code"])

        try:
            answer.delete()
            return HttpResponse(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            print(e)
            print("Line No: {0}".format(lineno()))
            return JSONError(message="Answer is not deleted", code=500)

@method_decorator(csrf_exempt, name='dispatch')
class UserAnswerList(APIView):
    """
    List all UserAnswers, or create a new UserAnswer.
    """
    def get(self, request, format=None):
        try:
            username_list = request.GET.getlist('user')
            user_answers = None
            if (len(username_list) == 0):
                user_answers = UserAnswer.objects.all()
            else:
                try:
                    user_id = int(username_list[0])
                    user_answers = UserAnswer.objects.filter(user=user_id)
                    if not user_answers.exists():
                        print("Line No: {0}".format(lineno()))
                        return JSONError(message= "User ID not Found", code=404)
                except ValueError as ve:
                    print(ve)
                    print("Line No: {0}".format(lineno()))
                    #User = get_user_model()
                    user = get_object_or_None(authUser, username=username_list[0])
                    if user is None:
                        print("Line No: {0}".format(lineno()))
                        return JSONError(message= "User ID not Found", code=404)
                    user_answers = UserAnswer.objects.filter(user=user.id)
                except UserAnswer.DoesNotExist:
                    print("Line No: {0}".format(lineno()))
                    return JSONError(message= "User ID not Found", code=404)
            user_answers_serializer = UserAnswerSerializerGet(user_answers,
                                                              many=True)
            return JSONResponse(user_answers_serializer.data)
        except Exception as e:
            print(e)
            print("Line No: {0}".format(lineno()))
            return JSONError(message="User Answer is not found", code=500)

    def post(self, request, format=None):
        try:
            user_answer_data = JSONParser().parse(request)
            if ('user' not in user_answer_data):
                print("Line No: {0}".format(lineno()))
                return JSONError("'user' key is not found in request data",
                                 code=400)
            else:
                if not isinstance(user_answer_data['user'], int):
                    print("Line No: {0}".format(lineno()))
                    return JSONError(message="'user' value is not an Integer",
                                     code=400)
                else:
                    #User = get_user_model()
                    user_obj = get_object_or_None(authUser, id=int(user_answer_data['user']))
                    if user_obj is None:
                        print("Line No: {0}".format(lineno()))
                        return JSONError(message="'user' object is not found",
                                         code=400)
            if ('question' not in user_answer_data):
                print("Line No: {0}".format(lineno()))
                return JSONError(message="'question' is not found in request data",
                                 code=400)
            else:
                if not isinstance(user_answer_data['question'], int):
                    print("Line No: {0}".format(lineno()))
                    return JSONError(message="'question' value is not an Integer",
                                     code=400)
                else:
                    user_obj = get_object_or_None(Question, id=int(user_answer_data['question']))
                    if user_obj is None:
                        print("Line No: {0}".format(lineno()))
                        return JSONError(message="'question' object is not found",
                                         code=400)

            if ('my_answer' not in user_answer_data):
                print("Line No: {0}".format(lineno()))
                return JSONError(message="'my_answer' is not found in request data",
                                 code=400)
            else:
                if not isinstance(user_answer_data['my_answer'], int):
                    print("Line No: {0}".format(lineno()))
                    return JSONError(message="'my_answer' value is not an Integer",
                                     code=400)
                else:
                    user_obj = get_object_or_None(Answer, id=int(user_answer_data['my_answer']))
                    if user_obj is None:
                        print("Line No: {0}".format(lineno()))
                        return JSONError(message="'my_answer' object is not found",
                                         code=400)

            if ('my_answer_importance' not in user_answer_data):
                print("Line No: {0}".format(lineno()))
                return JSONError(message="'my_answer_importance' is an not found in request data",
                                 code=400)
            else:
                if not isinstance(user_answer_data['my_answer_importance'], (str, unicode)):
                    print("Line No: {0}".format(lineno()))
                    return JSONError(message="'my_answer_importance' value is not String",
                                     code=400)

            if ('their_answer' not in user_answer_data):
                print("Line No: {0}".format(lineno()))
                return JSONError(message="'their_answer' is not found in request data",
                             code=400)
            else:
                if not isinstance(user_answer_data['their_answer'], int):
                    print("Line No: {0}".format(lineno()))
                    return JSONError(message="'their_answer' value is not an Integer",
                                     code=400)
                else:
                    user_obj = get_object_or_None(Answer, id=int(user_answer_data['their_answer']))
                    if user_obj is None:
                        print("Line No: {0}".format(lineno()))
                        return JSONError(message="'their_answer' object is not found",
                                         code=400)

            if ('their_importance' not in user_answer_data):
                print("Line No: {0}".format(lineno()))
                return JSONError(message="'their_importance' is not found in request data",
                             code=400)
            else:
                if not isinstance(user_answer_data['their_importance'], (str, unicode)):
                    print("Line No: {0}".format(lineno()))
                    return JSONError(message="'their_importance' value is not String",
                                     code=400)

            user_answer_serializer = UserAnswerSerializerPost(data=user_answer_data)
            if user_answer_serializer.is_valid():
                user_answer_serializer.save()
                return JSONResponse(user_answer_serializer.data,
                                    status=status.HTTP_201_CREATED)
            return JSONResponse(user_answer_serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            print("Line No: {0}".format(lineno()))
            return JSONError(message="User Answer is not created", code=500)

@method_decorator(csrf_exempt, name='dispatch')
class UserAnswerDetail(APIView):
    """
    Retrieve, update or delete an Answer instance.
    """
    def get_object(self, pk):
        try:
            usr_ans_id = int(pk)
            user_answer = get_object_or_None(UserAnswer, id=usr_ans_id)
        except ValueError as ve:
            print(ve)
            print("Line No: {0}".format(lineno()))
            return {"message":"UserAnswer ID value is not an Integer",
                    "code":400}
        if user_answer is None:
            return {"message":"UserAnswer is not found", "code":404}
        else:
            return user_answer


    def get(self, request, pk, format=None):
        user_answer = self.get_object(pk)
        if (isinstance(user_answer, dict) and
            ("message" in user_answer) and ("code" in user_answer) and
            (isinstance(user_answer["message"], (str, unicode))) and
            (isinstance(user_answer["code"], int))):
            print("Line No: {0}".format(lineno()))
            return JSONError(user_answer["message"], user_answer["code"])

        try:
            user_answer_serializer = UserAnswerSerializerGet(user_answer)
            return JSONResponse(user_answer_serializer.data)
        except Exception as e:
            print(e)
            print("Line No: {0}".format(lineno()))
            return JSONError(message="User Answer is not found", code=500)

    def put(self, request, pk, format=None):
        try:
            user_answer = self.get_object(pk)
            if (isinstance(user_answer, dict) and
                ("message" in user_answer) and ("code" in user_answer) and
                (isinstance(user_answer["message"], (str, unicode))) and
                (isinstance(user_answer["code"], int))):
                print("Line No: {0}".format(lineno()))
                return JSONError(user_answer["message"], user_answer["code"])

            user_answer_data = JSONParser().parse(request)
            if ('user' in user_answer_data):
                if not isinstance(user_answer_data['user'], int):
                    print("Line No: {0}".format(lineno()))
                    return JSONError(message="'user' value is not an Integer",
                                     code=400)
                else:
                    #User = get_user_model()
                    user_obj = get_object_or_None(authUser, id=int(user_answer_data['user']))
                    if user_obj is None:
                        print("Line No: {0}".format(lineno()))
                        return JSONError(message="'user' object is not found",
                                         code=400)
            if ('question' in user_answer_data):
                if not isinstance(user_answer_data['question'], int):
                    print("Line No: {0}".format(lineno()))
                    return JSONError(message="'question' value is not an Integer",
                                     code=400)
                else:
                    user_obj = get_object_or_None(Question, id=int(user_answer_data['question']))
                    if user_obj is None:
                        print("Line No: {0}".format(lineno()))
                        return JSONError(message="'question' object is not found",
                                         code=400)

            if ('my_answer' in user_answer_data):
                if not isinstance(user_answer_data['my_answer'], int):
                    print("Line No: {0}".format(lineno()))
                    return JSONError(message="'my_answer' value is not an Integer",
                                     code=400)
                else:
                    user_obj = get_object_or_None(Answer, id=int(user_answer_data['my_answer']))
                    if user_obj is None:
                        print("Line No: {0}".format(lineno()))
                        return JSONError(message="'my_answer' object is not found",
                                         code=400)

            if ('my_answer_importance' in user_answer_data):
                if not isinstance(user_answer_data['my_answer_importance'], (str, unicode)):
                    print("Line No: {0}".format(lineno()))
                    return JSONError(message="'my_answer_importance' value is not String",
                                     code=400)

            if ('their_answer' in user_answer_data):
                if not isinstance(user_answer_data['their_answer'], int):
                    print("Line No: {0}".format(lineno()))
                    return JSONError(message="'their_answer' value is not an Integer",
                                     code=400)
                else:
                    user_obj = get_object_or_None(Answer, id=int(user_answer_data['their_answer']))
                    if user_obj is None:
                        print("Line No: {0}".format(lineno()))
                        return JSONError(message="'their_answer' object is not found",
                                         code=400)

            if ('their_importance' in user_answer_data):
                if not isinstance(user_answer_data['their_importance'], (str, unicode)):
                    print("Line No: {0}".format(lineno()))
                    return JSONError(message="'their_importance' value is not String",
                                     code=400)

            user_answer_serializer = UserAnswerSerializerPost(user_answer,
                                                          data=user_answer_data,
                                                              partial=True)
            if user_answer_serializer.is_valid():
                user_answer_serializer.save()
                return JSONResponse(user_answer_serializer.data)
            return JSONResponse(user_answer_serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            print("Line No: {0}".format(lineno()))
            return JSONError(message="User Answer is not updated", code=500)

    def delete(self, request, pk, format=None):
        user_answer = self.get_object(pk)
        if (isinstance(user_answer, dict) and
            ("message" in user_answer) and ("code" in user_answer) and
            (isinstance(user_answer["message"], (str, unicode))) and
            (isinstance(user_answer["code"], int))):
            print("Line No: {0}".format(lineno()))
            return JSONError(user_answer["message"], user_answer["code"])

        try:
            user_answer.delete()
            return HttpResponse(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            print(e)
            print("Line No: {0}".format(lineno()))
            return JSONError(message="User Answer is not updated", code=500)
