from django.db import models
import uuid
from django.contrib.auth.models import User
import datetime as dt


# Create your models here.


class Task(models.Model):
    id = models.UUIDField(
        primary_key=True,
        null=False,
        unique=True,
        default=uuid.uuid4,
        editable=False,
    )
    user_id = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="users_task",
    )
    task_title = models.CharField(
        max_length=100,
        null=False,
    )
    task_description = models.TextField(
        max_length=300,
        null=True,
        blank=True,
    )
    is_important = models.BooleanField(
        default=False,
    )
    task_completed = models.BooleanField(
        default=False,
    )
    task_created_at = models.DateTimeField(
        auto_now_add=True,
    )
    task_updated_at = models.DateTimeField(
        auto_now=True,
    )
    task_due_date = models.DateTimeField(
        default=dt.datetime.now() + dt.timedelta(days=1),
    )

    def __str__(self) -> str:
        return str(self.task_title)

    def save(self, *args, **kwargs):
        if self.task_due_date is None:
            self.task_due_date = dt.datetime.now() + dt.timedelta(days=1)
        super(Task, self).save(*args, **kwargs)
