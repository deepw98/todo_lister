from rest_framework import serializers
from .models import Task,TodoList 

class ToDoListSerializer(serializers.ModelSerializer):
    class Meta:
        model = TodoList
        fields = '__all__'  # Includes all fields in the model

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__' 
