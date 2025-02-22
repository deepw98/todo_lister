from django.contrib import admin
from django.urls import path,include
from tdapp import views
from .views import TaskListCreateView, TaskDetailView,ToDoListViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'todo_lists', ToDoListViewSet, basename='todo_lists')

urlpatterns = [
    path("", views.index, name='tdapp'),  # Homepage or login/register page
    path("logout/", views.logout_view, name='logout'),  # Logout

    # To-Do List Management
    path("todo_lists/", views.todo_lists, name="todo_lists"),  # List of to-do lists
    path("add_todo_list/", views.add_todo_list, name="add_todo_list"),  # Add a new to-do list
    path("edit_todo_list/<int:list_id>/", views.edit_todo_list, name="edit_todo_list"),  # Edit a specific to-do list
    path("delete_todo_list/<int:list_id>/", views.delete_todo_list, name="delete_todo_list"),  # Delete a to-do list
    path("todo_lists/<int:list_id>/", views.todo_list_detail, name="todo_list_detail"),  # Tasks in a specific to-do list

    # Task Management
    path("list/<int:todo_list_id>/", views.list_view, name="list"),  # View tasks in a specific list
    path("add_task/<int:todo_list_id>/", views.add_task, name="add_task"),  # Add a task to a specific list
    path("delete/<int:task_id>/", views.delete_task, name="delete_task"),  # Delete a specific task
    path("toggle/<int:task_id>/", views.toggle_task, name="toggle_task"),  # Toggle task completion
    path("edit_task/<int:task_id>/", views.edit_task, name="edit_task"),  # Edit a task
    path("'todo_lists/<int:list_id>/'", views.todo_list_detail, name="task_list"),  # (Optional) View all tasks

    # Static Pages
    path("about/", views.about, name="about"),  # About page
    path("contact/", views.contact, name="contact"),  # Contact page

    # REST
    path('tasks/', TaskListCreateView.as_view(), name='task-list-create'),
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
    path('api/', include(router.urls))
]
