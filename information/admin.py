from django.contrib import admin
from models import Contact, Club, Department, EmergencyContact

class InformationAdmin(admin.ModelAdmin):
    list_display = ['title', 'link', 'phone']

admin.site.register(Contact, InformationAdmin)
admin.site.register(Club, InformationAdmin)
admin.site.register(Department, InformationAdmin)
admin.site.register(EmergencyContact, InformationAdmin)
