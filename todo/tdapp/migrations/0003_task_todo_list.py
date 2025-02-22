# Generated by Django 5.1.6 on 2025-02-21 03:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tdapp', '0002_todolist'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='todo_list',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='tdapp.todolist'),
            preserve_default=False,
        ),
    ]
