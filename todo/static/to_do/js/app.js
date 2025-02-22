async function fetchTasks() {
    try {
        let response = await fetch("http://127.0.0.1:8000/tasks/", {
            method: "GET",
            credentials: "include"  // 🔥 Ensures authentication cookies are sent
        });
        let tasks = await response.json();

        let taskList = document.getElementById("taskList");
        taskList.innerHTML = ""; // Clear existing tasks without removing layout

        tasks.forEach(task => {
            let listItem = document.createElement("li");
            listItem.classList.add("task-item"); // Apply CSS styles if needed
            listItem.innerHTML = `<span>${task.title} - ${task.completed ? "Yes" : "No"}</span>`;

            // Create Checkbox
            let checkbox = document.createElement("input");
            checkbox.type = "checkbox";
            checkbox.checked = task.completed;
            checkbox.addEventListener("change", () => updateTaskStatus(task.id, checkbox.checked));

            // Create Edit Button
            let editBtn = document.createElement("button");
            editBtn.textContent = "Edit";
            editBtn.classList.add("edit-btn"); 
            editBtn.addEventListener("click", () => editTask(task.id, task.title));

            // Create Delete Button
            let deleteBtn = document.createElement("button");
            deleteBtn.textContent = "Delete";
            deleteBtn.classList.add("delete-btn"); 
            deleteBtn.addEventListener("click", () => deleteTask(task.id));

            listItem.appendChild(checkbox);
            listItem.appendChild(editBtn);
            listItem.appendChild(deleteBtn);
            taskList.appendChild(listItem);
        });

    } catch (error) {
        console.error("Error fetching tasks:", error);
    }
}

// Function to edit task
function editTask(taskId, currentTitle) {
    let newTitle = prompt("Edit Task:", currentTitle);
    if (newTitle) {
        updateTaskTitle(taskId, newTitle);
    }
}

async function deleteTask(taskId) {
    try {
        const response = await fetch(`http://127.0.0.1:8000/tasks/${taskId}/`, {
            method: "DELETE",
            credentials: "include",
            headers: { "X-CSRFToken": getCSRFToken() }
        });

        if (response.ok) {
            console.log(`Task ${taskId} deleted successfully`);

            // Remove task from the DOM immediately
            let taskElement = document.getElementById(`task-${taskId}`);
            if (taskElement) {
                taskElement.remove();
            }

            fixTaskListStyles(); // Ensure layout remains correct
        } else {
            console.error("Failed to delete task:", response.status);
        }
    } catch (error) {
        console.error("Error deleting task:", error);
    }
}


function getCSRFToken() {
    let csrfToken = document.cookie.split("; ")
        .find(row => row.startsWith("csrftoken="))
        ?.split("=")[1];

    if (!csrfToken) {
        console.warn("CSRF token not found in cookies.");
    }
    return csrfToken;
}


tasks.forEach(task => {
    let listItem = document.createElement("li");
    listItem.id = `task-${task.id}`;  // ✅ Ensure each task has an ID
    listItem.classList.add("task-item");

    listItem.innerHTML = `
        <span>${task.title} - ${task.completed ? "Yes" : "No"}</span>
        <button class="delete-btn" onclick="deleteTask(${task.id})">Delete</button>
    `;

    taskList.appendChild(listItem);
});


// Function to update task title
async function updateTaskTitle(taskId, newTitle) {
    try {
        await fetch(`http://127.0.0.1:8000/tasks/${taskId}/`, {
            method: "PATCH",
            credentials: "include",
            headers: { 
                "Content-Type": "application/json",
                "X-CSRFToken": getCSRFToken()  // 🔥 CSRF token added
            },
            body: JSON.stringify({ title: newTitle }),
        });
        fetchTasks(); // Refresh task list
    } catch (error) {
        console.error("Error updating task:", error);
    }
}

document.addEventListener("DOMContentLoaded", function () {

    async function fetchTodoLists() {
        try {
            let response = await fetch("/api/todo_lists/", {
                method: "GET",
                credentials: "include"
            });
            let data = await response.json();
            displayTodoLists(data);
        } catch (error) {
            console.error("Error fetching to-do lists:", error);
        }
    }

    function displayTodoLists(todoLists) {
        const listContainer = document.querySelector(".display");
        listContainer.innerHTML = "";
        todoLists.forEach(todoList => {
            const listItem = document.createElement("li");
            listItem.innerHTML = `
                <a href="/tasks/${todoList.id}/" class="todo-link">${todoList.name}</a>
                <button class="edit-button" onclick="editTodoList(${todoList.id}, '${todoList.name}')">Edit</button>
                <button class="delete-button" onclick="deleteTodoList(${todoList.id})">Delete</button>
            `;
            listContainer.appendChild(listItem);
        });
    }

    async function addTodoList() {
        const nameInput = document.getElementById("todoListName");
        const name = nameInput.value.trim();

        if (!name) {
            alert("To-Do List name cannot be empty.");
            return;
        }

        try {
            const response = await fetch("/api/todo_lists/", {
                method: "POST",
                credentials: "include",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": getCSRFToken()
                },
                body: JSON.stringify({ name })
            });

            if (response.ok) {
                nameInput.value = "";  // Clear input field after success
                fetchTodoLists();  // Refresh the to-do list
            } else {
                console.error("Failed to add to-do list:", await response.json());
                alert("Error adding to-do list.");
            }
        } catch (error) {
            console.error("Error adding to-do list:", error);
        }
    }

    async function deleteTodoList(id) {
        try {
            const response = await fetch(`/api/todo_lists/${id}/`, {
                method: "DELETE",
                credentials: "include",
                headers: { "X-CSRFToken": getCSRFToken() }
            });
            if (response.ok) {
                fetchTodoLists();
            }
        } catch (error) {
            console.error("Error deleting to-do list:", error);
        }
    }

    async function editTodoList(id, currentName) {
        const newName = prompt("Edit list name:", currentName);
        if (newName) {
            try {
                const response = await fetch(`/api/todo_lists/${id}/`, {
                    method: "PUT",
                    credentials: "include",
                    headers: {
                        "Content-Type": "application/json",
                        "X-CSRFToken": getCSRFToken()
                    },
                    body: JSON.stringify({ name: newName })
                });
                if (response.ok) {
                    fetchTodoLists();
                }
            } catch (error) {
                console.error("Error editing to-do list:", error);
            }
        }
    }

    function getCSRFToken() {
        let csrfToken = document.cookie.split("; ")
            .find(row => row.startsWith("csrftoken="))
            ?.split("=")[1];

        if (!csrfToken) {
            console.warn("CSRF token not found in cookies.");
        }
        return csrfToken;
    }

    document.getElementById("addTodoListButton").addEventListener("click", addTodoList);
    
    fetchTodoLists();
});
