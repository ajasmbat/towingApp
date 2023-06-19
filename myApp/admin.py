from django.contrib import admin
from myApp.models import MyUser, Location
from django.contrib.auth.admin import UserAdmin






admin.site.register(MyUser)
admin.site.register(Location)