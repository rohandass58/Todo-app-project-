from django.contrib import admin
from todo_app.models import Task
from django.contrib.auth.admin import UserAdmin
from .models import User, Task


class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user_id",
        "task_title",
        "is_important",
        "task_completed",
        "task_due_date",
    )
    list_filter = (
        "user_id",
        "is_important",
        "task_completed",
    )
    search_fields = (
        "user_id__username",
        "task_title",
    )


admin.site.register(Task, TaskAdmin)
