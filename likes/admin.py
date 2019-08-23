from django.contrib import admin

# Register your models here.

from likes.models import UserLike


admin.site.register(UserLike)
