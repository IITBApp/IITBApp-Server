from django.contrib import admin
from models import Designation


class DesignationAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'post', 'start_date', 'end_date']


admin.site.register(Designation, DesignationAdmin)
