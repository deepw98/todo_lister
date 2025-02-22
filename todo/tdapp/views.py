from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import Task,TodoList
from django.http import JsonResponse
import json
from rest_framework import generics
from .serializers import TaskSerializer, ToDoListSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

def index(request):
    if request.user.is_authenticated:
        return redirect('todo_lists')  # Redirect to the list page if already logged in

    if request.method == "POST":
        # Handle registration
        if 'register' in request.POST:
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            username = request.POST.get('username')
            password = request.POST.get('password')

            if User.objects.filter(username=username).exists():
                return render(request, 'index.html', {
                    'error_register': 'Username already exists',
                    'first_name': first_name,
                    'last_name': last_name,
                    'username': username
                })
            
            try:
                validate_password(password)
            except ValidationError as e:
                return render(request, 'index.html', {
                    'error_register': ' '.join(e.messages),
                    'first_name': first_name,
                    'last_name': last_name,
                    'username': username
                })

            # Create user
            user = User.objects.create_user(
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            user.save()
            return render(request, 'index.html', {'success_register': 'Registration successful! Please log in.'})

        # Handle login
        elif 'login' in request.POST:
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('todo_lists')  # Redirect to the list page after login
            else:
                return render(request, 'index.html', {'error_login': 'Invalid credentials'})

    return render(request, 'index.html')  # Render the page for GET requests

def logout_view(request):
    logout(request)
    return redirect('tdapp')  # Redirect to the homepage or login page after logout

@login_required
def list_view(request, todo_list_id):
    # Get the TodoList object
    todo_list = get_object_or_404(TodoList, id=todo_list_id)

    if request.method == "POST":
        # Get the task title from the form data
        new_task_title = request.POST.get("new_task")
        if new_task_title:  # Ensure it's not empty
            # Create a new Task object and associate it with the current TodoList
            Task.objects.create(title=new_task_title, todo_list=todo_list)
            return redirect("list", todo_list_id=todo_list.id)

    # Get all tasks associated with this TodoList
    tasks = Task.objects.filter(todo_list=todo_list)

    # Pass the TodoList and tasks to the template
    context = {
        "todo_list": todo_list,
        "tasks": tasks,
    }
    return render(request, "list.html", context)

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def todo_lists(request):
    todo_lists = TodoList.objects.all()
    return render(request, 'todo_lists_manage.html', {'todo_lists': todo_lists})

def add_todo_list(request):
    if request.method == "POST":
        name = request.POST['name']
        TodoList.objects.create(name=name)
        return redirect('todo_lists')
    return render(request, 'todo_lists_manage.html', {'adding': True})

def edit_todo_list(request, list_id):
    todo_list = get_object_or_404(TodoList, id=list_id)
    if request.method == "POST":
        new_name = request.POST['name']
        todo_list.name = new_name
        todo_list.save()
        return redirect('todo_lists')
    return render(request, 'todo_lists_manage.html', {'editing': True, 'todo_list': todo_list})


# View to delete a to-do list
def delete_todo_list(request, list_id):
    todo_list = get_object_or_404(TodoList, id=list_id)
    if request.method == "POST":
        todo_list.delete()
    return redirect('todo_lists')

# View to display tasks for a specific to-do list
def task_list(request, list_id):
    todo_list = get_object_or_404(TodoList, id=list_id)
    tasks = todo_list.tasks.all()
    return render(request, 'list.html', {'tasks': tasks, 'todo_list': todo_list})

def delete_task(request, task_id):
    if request.method == "POST":
        task = get_object_or_404(Task, id=task_id)
        task.delete()
    return redirect('task_list')

def todo_list_detail(request, list_id):
    todo_list = get_object_or_404(TodoList, id=list_id)  # Fetch specific to-do list
    if request.method == "POST":
        if "task" in request.POST:  # Adding a new task
            task_title = request.POST["task"]
            Task.objects.create(title=task_title, todo_list=todo_list)
        elif "task_id" in request.POST:  # Deleting a task
            task_id = request.POST["task_id"]
            Task.objects.filter(id=task_id, todo_list=todo_list).delete()

    tasks = todo_list.tasks.all()  # Get tasks for this to-do list
    return render(request, "list.html", {"tasks": tasks, "todo_list": todo_list})

def task_list(request):
    tasks = Task.objects.all()
    return render(request, 'list.html', {'tasks': tasks})

def add_task(request, list_id):
    todo_list = get_object_or_404(TodoList, id=list_id)
    if request.method == "POST":
        title = request.POST['title']
        Task.objects.create(title=title, todo_list=todo_list)
        return redirect('todo_list_detail', todo_list_id=list_id)
    return redirect('todo_list_detail', todo_list_id=list_id)
  # Redirect back to the list view

def edit_task(request, task_id):
    """Edit a task's title."""
    if request.method == "POST":
        data = json.loads(request.body)
        task_title = data.get("title")

        try:
            task = Task.objects.get(id=task_id)
            task.title = task_title
            task.save()
            return JsonResponse({"success": True, "updated_title": task.title})
        except Task.DoesNotExist:
            return JsonResponse({"success": False, "error": "Task not found"})

    return JsonResponse({"success": False, "error": "Invalid request method"})


def toggle_task(request, task_id):
    """Toggle a task's completion status."""
    if request.method == "POST":
        data = json.loads(request.body)
        completed = data.get("completed")

        try:
            task = Task.objects.get(id=task_id)
            task.completed = completed
            task.save()
            return JsonResponse({"success": True})
        except Task.DoesNotExist:
            return JsonResponse({"success": False, "error": "Task not found"})

    return JsonResponse({"success": False, "error": "Invalid request method"})



######  REST API #######

class TaskListCreateView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_tasks(request, list_id):
    tasks = Task.objects.filter(todo_list_id=list_id)
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)

class ToDoListViewSet(viewsets.ModelViewSet):
    queryset = TodoList.objects.all()
    serializer_class = ToDoListSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)  


def get_todolists(request):
    return JsonResponse({"message": "Success!"})


