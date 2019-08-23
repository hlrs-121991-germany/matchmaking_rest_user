from rest_framework import serializers
from matches.models import Match
from matches.models import PositionMatch
from matches.models import EmployerMatch
from matches.models import LocationMatch


class MatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = [
            'id',
            'user_a',
            'user_b',
            'match_decimal',
            'questions_answered',
            'timestamp',
            'updated',
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

