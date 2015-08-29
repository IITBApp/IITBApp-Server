from django.contrib import admin

from .models import Device


class DeviceAdmin(admin.ModelAdmin):
    list_display = ['dev_id', 'user', 'last_modified', 'is_active']
    search_fields = ('dev_id', 'user')
    list_filter = ['is_active']
    date_hierarchy = 'last_modified'
    readonly_fields = ('dev_id', 'reg_id')


admin.site.register(Device, DeviceAdmin)
