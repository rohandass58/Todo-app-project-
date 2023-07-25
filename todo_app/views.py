from typing import Any, Dict
from django.forms.models import BaseModelForm
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy

from .models import Task

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

# Create your views here.

from django.views import View
from django.shortcuts import redirect
from django.db import transaction
from .forms import PositionForm

# def task_list(request):
#     return HttpResponse("this is taks list")


class CustomLoginView(LoginView):
    template_name = "todo_app/login.html"
    fields = "__all__"
    redirect_authenticated_user = True

    def get_success_url(self) -> str:
        return reverse_lazy("tasks")


class RegisterPage(FormView):
    template_name = "todo_app/register.html"
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy("tasks")

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args: str, **kwargs: Any):
        if self.request.user.is_authenticated:
            return redirect("tasks")
        return super(RegisterPage, self).get(*args, **kwargs)


class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = "tasks"

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        context["tasks"] = context["tasks"].filter(user_id=self.request.user)
        context["count"] = context["tasks"].filter(task_completed=False).count()

        return context


class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = "task_detail"


class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = [
        "task_title",
        "task_description",
        "is_important",
        "task_completed",
        "task_due_date",
    ]
    success_url = reverse_lazy("tasks")

    def form_valid(self, form):
        form.instance.user_id = self.request.user
        return super(TaskCreate, self).form_valid(form)


class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = [
        "task_title",
        "task_description",
        "is_important",
        "task_completed",
        "task_due_date",
    ]
    success_url = reverse_lazy("tasks")


class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = "tasks"
    success_url = reverse_lazy("tasks")


class TaskReorder(View):
    def post(self, request):
        form = PositionForm(request.POST)

        if form.is_valid():
            positionList = form.cleaned_data["position"].split(",")

            with transaction.atomic():
                self.request.user.set_task_order(positionList)

        return redirect(reverse_lazy("tasks"))
