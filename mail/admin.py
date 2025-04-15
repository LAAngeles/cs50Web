from django.contrib import admin

from .models import *
# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email")

class EmailsAdmin(admin.ModelAdmin):
    filter_horizontal = ("recipients",)


admin.site.register(User,UserAdmin)
admin.site.register(Email,EmailsAdmin)