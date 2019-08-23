from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User as authUser
from rest_framework import serializers
from likes.models import UserLike

User = settings.AUTH_USER_MODEL

class CurrentUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = authUser
        fields = [
            'id',
            'username',
        ]

class UserLikeSerializer(serializers.ModelSerializer):
    user = CurrentUserSerializer(many=False)
    #user = serializers.PrimaryKeyRelatedField(queryset=User)
    liked_users = CurrentUserSerializer(many=True)
    #liked_users = serializers.PrimaryKeyRelatedField(queryset=User, many=True)
    class Meta:
        model = UserLike
        fields = [
            'user',
            'liked_users',
        ]
        depth = 2
