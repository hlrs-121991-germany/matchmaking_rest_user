from django.db import models
from django.contrib.auth.models import User

# Create your models here.
#class User(models.Model):
#    username = models.TextField(max_length=300, unique=True)

#    def __str__(self):
#        return self.username

from mozilla_django_oidc.auth import OIDCAuthenticationBackend

class MyOIDCAB(OIDCAuthenticationBackend):
    def create_user(self, claims):
        user = super(MyOIDCAB, self).create_user(claims)

        user.first_name = claims.get('given_name', '')
        user.last_name = claims.get('family_name', '')
        user.username = claims.get('preferred_username', '')

        user.save()

        return user

    def update_user(self, user, claims):
        user.first_name = claims.get('given_name', '')
        user.last_name = claims.get('family_name', '')
        user.username = claims.get('preferred_username', '')
        user.save()

        return user
