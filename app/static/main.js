function deleteTask(taskId) {
    fetch(`/delete/${taskId}`, {
        method: 'DELETE',
    })
    .then(response => {
        if (response.ok) {
            location.reload();
        } else {
            alert('Failed to delete task');
        }
    });
}