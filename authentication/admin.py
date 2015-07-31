from django.contrib import admin
from models import Designation, UserToken


class DesignationAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'post', 'start_date', 'end_date']


class UserTokenAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'token', 'created', 'last_accessed']

admin.site.register(Designation, DesignationAdmin)
admin.site.register(UserToken, UserTokenAdmin)
