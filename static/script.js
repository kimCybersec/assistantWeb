document.addEventListener('DOMContentLoaded', function() {
    // Track currently open tab
    let currentOpenTab = null;
    
    // Tab functionality with improved mobile support
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
                    const rect = content.getBoundingClientRect();
                    const isContentBelowViewport = rect.bottom > (window.innerHeight || document.documentElement.clientHeight);
                    const isContentAboveViewport = rect.top < 0;
                    
                    if (isContentBelowViewport || isContentAboveViewport) {
                        content.scrollIntoView({ 
                            behavior: 'smooth', 
                            block: 'nearest'
                        });
                    }
                }, 100);
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
        } else if (window.innerWidth <= 768 && currentOpenTab) {
            currentOpenTab.classList.remove('active');
            currentOpenTab.previousElementSibling.querySelector('.toggle-icon').textContent = '+';
            currentOpenTab = null;
        }
    });

    // Enhanced touch support
    if ('ontouchstart' in window) {
        document.body.classList.add('touch-device');
        
        // Add slight delay to prevent accidental double-taps
        dayButtons.forEach(btn => {
            let lastTouchTime = 0;
            btn.addEventListener('touchend', function(e) {
                const currentTime = new Date().getTime();
                if (currentTime - lastTouchTime < 300) {
                    e.preventDefault();
                    return;
                }
                lastTouchTime = currentTime;
            }, {passive: false});
        });

        // Add touch-specific styles
        const style = document.createElement('style');
        style.textContent = `
            .touch-device .day-btn {
                padding: 1rem 2.5rem 1rem 1rem;
                min-height: 48px;
            }
            .touch-device .task-item {
                min-height: 44px;
                padding: 0.8rem 1rem;
            }
            .day-btn.touch-active {
                transform: scale(0.98) !important;
                opacity: 0.9 !important;
            }
            .touch-device input[type="checkbox"] {
                width: 22px;
                height: 22px;
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