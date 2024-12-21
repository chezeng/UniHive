from django.urls import path, re_path
from . import views

app_name = "forum"

urlpatterns = [
    path('', views.task_list, name="task_list"),
    path('create/', views.create_task, name="create_task"),
    path('update/<int:pk>/', views.update_task, name="update_task"),
    path('delete/<int:pk>/', views.delete_task, name="delete_task"),
]
