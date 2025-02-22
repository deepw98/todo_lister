document.addEventListener("DOMContentLoaded", () => {
  // Function to handle toggling edit mode
  const toggleEditMode = (taskRow, isEditing) => {
      const taskTitleElement = taskRow.querySelector(".task-title");
      const editInputElement = taskRow.querySelector(".edit-input");
      const editButton = taskRow.querySelector(".edit-button");
      const saveButton = taskRow.querySelector(".save-button");

      if (isEditing) {
          // Switch to editing mode
          taskTitleElement.style.display = "none";
          editInputElement.style.display = "inline";
          editInputElement.value = taskTitleElement.textContent.trim();
          editInputElement.focus();
          editButton.style.display = "none";
          saveButton.style.display = "inline";
      } else {
          // Switch back to normal mode
          taskTitleElement.style.display = "inline";
          editInputElement.style.display = "none";
          editButton.style.display = "inline";
          saveButton.style.display = "none";
      }
  };

  // Edit button functionality
  document.querySelectorAll(".edit-button").forEach(editButton => {
      editButton.addEventListener("click", function () {
          const taskRow = this.closest(".task-row");
          toggleEditMode(taskRow, true);
      });
  });

  // Save button functionality
  document.querySelectorAll(".save-button").forEach(saveButton => {
      saveButton.addEventListener("click", function () {
          const taskRow = this.closest(".task-row");
          const taskId = this.getAttribute("data-task-id");
          const editInputElement = taskRow.querySelector(".edit-input");
          const taskTitleElement = taskRow.querySelector(".task-title");

          const updatedTitle = editInputElement.value;

          // Send updated title to the server
          fetch(`/edit_task/${taskId}/`, {
              method: "POST",
              headers: {
                  "Content-Type": "application/json",
                  "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value
              },
              body: JSON.stringify({ title: updatedTitle })
          })
              .then(response => response.json())
              .then(data => {
                  if (data.success) {
                      // Update the task title in the UI
                      taskTitleElement.textContent = data.updated_title;
                      toggleEditMode(taskRow, false);
                  } else {
                      alert("Failed to update the task. Please try again.");
                  }
              })
              .catch(err => console.error("Error updating task:", err));
      });
  });
});
