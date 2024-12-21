from django.shortcuts import get_object_or_404, render, redirect, get_list_or_404
from django.urls import reverse
from .models import Task
from .forms import TaskForm

# Create a task
def create_task(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse("create_task"))
    else:
        form = TaskForm()
    return render(request, "forum/create_task.html", {"form": form})


# Retrieve task list
def task_list(request):
    tasks = Task.objects.all()
    return render(request, "forum/task_list.html", {"tasks": tasks})


# Update a task
def update_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect("task_list")
    else:
        form = TaskForm(instance=task)
    return render(request, "forum/update_task.html", {"form": form})


# Delete a task
def delete_task(request, pk):
    task = get_object_or_404(pk=pk)
    if request.method == 'POST':
        task.delete()
        return redirect("task_list")
    return render(request, 'forum/delete_task.html', {'task': task})


