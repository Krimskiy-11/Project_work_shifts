from django.contrib import admin
from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "status", "assigned_to", "created_by", "created_at", "due_date")
    list_filter = ("status", "created_at", "assigned_to")
    search_fields = ("title", "description", "assigned_to__username", "created_by__username")
    raw_id_fields = ("assigned_to", "created_by")
