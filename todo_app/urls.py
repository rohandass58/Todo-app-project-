from django.urls import path, include
from .views import (
    TaskList,
    TaskDetail,
    TaskCreate,
    TaskUpdate,
    TaskDelete,
    CustomLoginView,
    RegisterPage,
    TaskReorder,
)
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(next_page="login"), name="logout"),
    path("register/", RegisterPage.as_view(), name="register"),
    path("", TaskList.as_view(), name="tasks"),
    path("task/<uuid:pk>/", TaskDetail.as_view(), name="task_detail"),
    path("task-create/", TaskCreate.as_view(), name="task-create"),
    path("task-update/<uuid:pk>/", TaskUpdate.as_view(), name="task_update"),
    path("task-delete/<uuid:pk>/", TaskDelete.as_view(), name="task_delete"),
    path("task-reorder/", TaskReorder.as_view(), name="task-reorder"),
]
