from django.contrib import admin

from projects.models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ["name", "owner", "status", "created_at"]
    search_fields = ["name", "owner__email"]
    list_filter = ["status"]
    readonly_fields = ["created_at"]
