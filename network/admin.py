from django.contrib import admin

from .models import *
# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email")

class PostAdmin(admin.ModelAdmin):
    filter_horizontal = ("likes",)

class FollowerAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "userYouFollowId", "follow", "timestamp")

class LikeAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "post_id", "likeUnlike", "timestamp")

admin.site.register(User,UserAdmin)
admin.site.register(Post,PostAdmin)
admin.site.register(Like,LikeAdmin)
admin.site.register(Follower,FollowerAdmin)