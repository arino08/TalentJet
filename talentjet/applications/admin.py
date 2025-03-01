from django.contrib import admin
from .models import Application

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('job', 'applicant', 'applied_at', 'status')
    list_filter = ('status', 'applied_at')
    search_fields = ('job__title', 'applicant__username', 'applicant__email')
    date_hierarchy = 'applied_at'
