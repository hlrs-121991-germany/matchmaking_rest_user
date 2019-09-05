from rest_framework import serializers
from users.models import User as authUser
from matches.models import Match
from matches.models import PositionMatch
from matches.models import EmployerMatch
from matches.models import LocationMatch
#from django.contrib.auth.models import User as authUser
from users.models import User as authUser


class CurrentUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = authUser
        fields = [
            'id',
            'username',
        ]


class MatchSerializer(serializers.ModelSerializer):
    user_a = CurrentUserSerializer(many=False)
    user_b = CurrentUserSerializer(many=False)
    class Meta:
        model = Match
        fields = [
            'id',
            'user_a',
            'user_b',
            'match_decimal',
            'questions_answered',
        ]

class PositionMatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = PositionMatch
        fields = [
            'id',
            'user',
            'job',
            'hidden',
            'liked',
        ]

class EmployerMatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployerMatch
        fields = [
            'id',
            'user',
            'employer',
            'hidden',
            'liked',
        ]

class LocationMatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocationMatch
        fields = [
            'id',
            'user',
            'location',
            'hidden',
            'liked',
        ]

