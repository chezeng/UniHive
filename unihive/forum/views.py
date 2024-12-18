from django.shortcuts import render, redirect, get_list_or_404
from django.urls import reverse
from .models import Task
from .forms import TaskForm

# Create a task
def task_create(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse("forum:task_list"))
    else:
        form = TaskForm()
    return render(request, "forum/task_create.html", {"form": form})


# Retrieve task list
def task_list(request):
    tasks = Task.objects.all()
    return render(request, "forum/task_list.html", {"tasks": tasks})


# Retrieve task detail
def task_detail(request, pk):
    task = Task.objects.get(pk=pk)
    return render(request, "forum/task_detail.html", {"task": task})


# Update a task
def task_update(request, pk):
    task = get_list_or_404(pk=pk)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect(reverse("forum:task_list"))
    else:
        form = TaskForm(instance=task)
    return render(request, "forum/task_update.html", {"form": form})


# Delete a task
def task_delete(request, pk):
    task = get_list_or_404(pk=pk)
    task.delete()
    return redirect(reverse("forum:task_list"))
