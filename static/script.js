document.addEventListener('DOMContentLoaded', function() {
    // Track currently open tab
    let currentOpenTab = null;
    
    // Tab functionality with mobile support
    const dayButtons = document.querySelectorAll('.day-btn');
    dayButtons.forEach(button => {
        button.addEventListener('click', function() {
            const content = this.nextElementSibling;
            const icon = this.querySelector('.toggle-icon');
            const isOpening = !content.classList.contains('active');
            
            // Close previously open tab
            if (currentOpenTab && currentOpenTab !== content) {
                currentOpenTab.classList.remove('active');
                const prevIcon = currentOpenTab.previousElementSibling.querySelector('.toggle-icon');
                prevIcon.textContent = '+';
            }
            
            // Toggle current tab
            content.classList.toggle('active', isOpening);
            icon.textContent = isOpening ? '−' : '+';
            currentOpenTab = isOpening ? content : null;
            
            // Mobile-specific adjustments
            if (window.innerWidth <= 768 && isOpening) {
                setTimeout(() => {
                    content.scrollIntoView({ 
                        behavior: 'smooth', 
                        block: 'nearest'
                    });
                }, 50);
            }
        });
    });

    // Task completion functionality with loading states
    document.querySelectorAll('input[type="checkbox"]').forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            const taskItem = this.closest('.task-item');
            taskItem.classList.add('updating');
            
            if (this.checked) {
                taskItem.classList.add('task-done');
            } else {
                taskItem.classList.remove('task-done');
            }
            
            updateTaskStatus(this)
                .finally(() => {
                    taskItem.classList.remove('updating');
                });
        });
    });

    // Initialize first tab as open on desktop
    if (window.innerWidth > 768 && dayButtons.length > 0) {
        dayButtons[0].click();
    }
    
    // Handle window resize
    window.addEventListener('resize', function() {
        if (window.innerWidth > 768 && !currentOpenTab && dayButtons.length > 0) {
            dayButtons[0].click();
        }
    });

    // Enhanced touch support
    if ('ontouchstart' in window) {
        document.body.classList.add('touch-device');
        
        dayButtons.forEach(btn => {
            btn.addEventListener('touchstart', function(e) {
                this.classList.add('touch-active');
                e.preventDefault();
            }, {passive: false});
            
            btn.addEventListener('touchend', function() {
                this.classList.remove('touch-active');
            });
        });

        // Add touch-specific styles
        const style = document.createElement('style');
        style.textContent = `
            .touch-device .day-btn {
                padding: 1rem 1.2rem;
                min-height: 48px;
            }
            .touch-device .task-item {
                min-height: 48px;
                padding: 0.8rem 1rem;
            }
            .day-btn.touch-active {
                transform: scale(0.98) !important;
                opacity: 0.9 !important;
            }
        `;
        document.head.appendChild(style);
    }
});

async function updateTaskStatus(checkbox) {
    const day = checkbox.name.replace('task_', '');
    const taskTitle = checkbox.value;
    const status = checkbox.checked ? 'done' : 'pending';
    const taskItem = checkbox.closest('.task-item');
    
    try {
        const response = await fetch('/update-task', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                day: day,
                taskTitle: taskTitle,
                status: status
            })
        });
        
        if (!response.ok) {
            throw new Error('Update failed');
        }
        
        const data = await response.json();
        if (!data.success) {
            throw new Error('Server reported failure');
        }
        
    } catch (error) {
        console.error('Error:', error);
        // Revert visual change
        checkbox.checked = !checkbox.checked;
        taskItem.classList.toggle('task-done');
        
        // Show error to user (optional)
        const errorMsg = document.createElement('div');
        errorMsg.className = 'error-message';
        errorMsg.textContent = 'Failed to update. Please try again.';
        taskItem.appendChild(errorMsg);
        
        setTimeout(() => {
            errorMsg.remove();
        }, 3000);
    }
}