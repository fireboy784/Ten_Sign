from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from api.models import  Lead

# Lead Admin
class LeadAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email')

admin.site.register(Lead, LeadAdmin)

