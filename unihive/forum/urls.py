from django.urls import path, re_path
from . import views

app_name = "forum"

urlpatterns = [
    # Create a task
    path("create/", views.create_task, name="task_create"),

    # Retrieve task list
    path("", views.task_list, name="task_list"),

    # Retrieve a single task
    re_path(r"^(?P<pk>\d+)/$", views.task_detail, name="task_detail"),

    # Update a task
    re_path(r"^(?P<pk>\d+)/update/$", views.update_task, name="task_update"),

    # Delete a task
    re_path(r"^(?P<pk>\d+)/delete/$", views.delete_task, name="task_delete"),
]
