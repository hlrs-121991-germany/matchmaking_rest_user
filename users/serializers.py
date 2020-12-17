from django.conf import settings
# from django.contrib.auth import User
from rest_framework import serializers
from django.contrib.auth.models import User as authUser
#from users.models import User as authUser 

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = authUser
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
        ]
