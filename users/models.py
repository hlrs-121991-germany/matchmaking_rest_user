from django.db import models
#from django.contrib.auth.models import User

# Create your models here.
class User(models.Model):
    username = models.TextField(max_length=300, unique=True)

    def __str__(self):
        return self.username

