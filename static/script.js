document.addEventListener('DOMContentLoaded', function() {
    // Tab functionality
    const dayButtons = document.querySelectorAll('.day-btn');
    dayButtons.forEach(button => {
        button.addEventListener('click', function() {
            const content = this.nextElementSibling;
            const icon = this.querySelector('.toggle-icon');
            
            // Toggle current day
            content.classList.toggle('active');
            icon.textContent = content.classList.contains('active') ? '−' : '+';
        });
    });

    // Task completion functionality
    document.querySelectorAll('input[type="checkbox"]').forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            const taskItem = this.closest('.task-item');
            if (this.checked) {
                taskItem.classList.add('task-done');
                // Send update to server
                updateTaskStatus(this);
            } else {
                taskItem.classList.remove('task-done');
                // Send update to server
                updateTaskStatus(this);
            }
        });
    });

    // Initialize first day as open by default
    if (dayButtons.length > 0) {
        dayButtons[0].click();
    }

    // Add touch event support
    document.querySelectorAll('.day-btn').forEach(btn => {
        // Add touch support
        btn.addEventListener('touchstart', function(e) {
            this.classList.add('touch-active');
            e.preventDefault();
        }, {passive: false});
        
        btn.addEventListener('touchend', function() {
            this.classList.remove('touch-active');
        });
    });

    // Better touch feedback
    const style = document.createElement('style');
    style.textContent = `
        .day-btn.touch-active {
            transform: scale(0.98) !important;
            opacity: 0.9 !important;
        }
    `;
    document.head.appendChild(style);
});

function updateTaskStatus(checkbox) {
    const day = checkbox.name.replace('task_', '');
    const taskTitle = checkbox.value;
    const status = checkbox.checked ? 'done' : 'pending';
    
    fetch('/update-task', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            day: day,
            taskTitle: taskTitle,
            status: status
        })
    }).then(response => {
        if (!response.ok) {
            throw new Error('Update failed');
        }
        return response.json();
    }).then(data => {
        if (!data.success) {
            throw new Error('Server reported failure');
        }
    }).catch(error => {
        console.error('Error:', error);
        // Revert visual change if update failed
        checkbox.checked = !checkbox.checked;
        const taskItem = checkbox.closest('.task-item');
        taskItem.classList.toggle('task-done');
    });
}