from django.contrib import admin

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["email", "name", "surname", "is_active", "is_staff"]
    search_fields = ["email", "name", "surname"]
    list_filter = ["is_active", "is_staff"]
