from django.contrib import admin
from users import models as user_models


class UserAdmin(admin.ModelAdmin):
    list_display = ['first_name']


admin.site.register(user_models.User, UserAdmin)
