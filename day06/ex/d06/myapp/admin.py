from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserTip


admin.site.register(UserTip)
