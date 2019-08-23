from rest_framework import serializers
from questions.models import Question
from questions.models import Answer
from questions.models import UserAnswer


# serializers.Serializer to serialize the QuestionSerializer
#
#    id = serializers.IntegerField(read_only=True)
#    text = serializers.CharField()
#    active = serializers.BooleanField(required=True)
#    draft = serializers.BooleanField(required=False)
#    timestamp = serializers.DateTimeField()

#    def create(self, validated_data):
#        return Question.objects.create(**validated_data)

#    def update(self, instance, validated_data):
#        instance.text = validated_data.get('text', instance.text)
#        instance.active = validated_data.get('active', instance.active)
#        instance.draft = validated_data.get('draft', instance.draft)
#        instance.timestamp = validated_data.get('timestamp', instance.timestamp)
#        instance.save()
#        return instance


class AnswerSerializer(serializers.ModelSerializer):
#    question = QuestionSerializer(many=False)
    class Meta:
        model = Answer
        fields = [
            'id',
#            'question',
            'text',
#            'active',
#            'draft',
#            'timestamp'
        ]
        depth = 2

class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True)
    class Meta:
        model = Question
        fields = [
            'id',
            'text',
            'answers',
#            'active',
#            'draft',
#            'timestamp'
        ]

class CustomQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = [
            'id',
            'text',
#            'answers',
#            'active',
#            'draft',
#            'timestamp'
        ]



class UserAnswerSerializer(serializers.ModelSerializer):
    my_answer = AnswerSerializer(many=False)
    their_answer = AnswerSerializer(many=False)
    question = CustomQuestionSerializer(many=False)
    class Meta:
        model = UserAnswer
        fields = [
            'id',
            'user',
            'question',
            'my_answer',
            'my_answer_importance',
            'my_points',
            'their_answer',
            'their_importance',
            'their_points',
#            'timestamp'
        ]


