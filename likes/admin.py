from django.contrib import admin

# Register your models here.

from likes.models import UserLike

class UserLikeAdmin(admin.ModelAdmin):
    exclude = ("add", "remove")

admin.site.register(UserLike, UserLikeAdmin)
