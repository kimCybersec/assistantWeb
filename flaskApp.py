from flask import Flask, render_template_string, request, redirect, url_for
from utils.gptScheduler import generateSchedule, saveSChedule
from utils.tracker import showAllTasks, markDone, showSummary
import json

app = Flask(__name__)

# HTML template for the web interface
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Schedule Assistant</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
        .menu { margin-bottom: 20px; }
        .task-list { margin-top: 20px; }
        .task { padding: 5px; border-bottom: 1px solid #eee; }
        .done { text-decoration: line-through; color: #888; }
    </style>
</head>
<body>
    <h1>Weekly Scheduler and Task Tracker</h1>
    
    <div class="menu">
        <a href="{{ url_for('index') }}">Home</a> |
        <a href="{{ url_for('generate') }}">Generate Schedule</a> |
        <a href="{{ url_for('show_tasks') }}">Show All Tasks</a> |
        <a href="{{ url_for('show_summary') }}">Show Summary</a>
    </div>
    
    {% block content %}{% endblock %}
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE + """
        <h2>Welcome to Schedule Assistant</h2>
        <p>Use the menu above to navigate.</p>
    """)

@app.route('/generate', methods=['GET', 'POST'])
def generate():
    if request.method == 'POST':
        goal = request.form['goal']
        schedule = generateSchedule(goal)
        if schedule:
            saveSChedule(schedule)
            return redirect(url_for('show_tasks'))
    
    return render_template_string(HTML_TEMPLATE + """
        <h2>Generate Schedule</h2>
        <form method="POST">
            <label for="goal">What is your goal for this week?</label><br>
            <input type="text" id="goal" name="goal" required style="width: 100%; padding: 8px;"><br><br>
            <input type="submit" value="Generate Schedule">
        </form>
    """)

@app.route('/tasks')
def show_tasks():
    schedule = json.load(open('data/schedule.json'))
    tasks_html = ""
    for day, tasks in schedule.items():
        tasks_html += f"<h3>{day}</h3>"
        for task in tasks:
            if isinstance(task, dict):
                status = "done" if task.get("status") == "done" else "pending"
                tasks_html += f'<div class="task {status}">- {task.get("title", "")} [{status}]</div>'
            else:
                tasks_html += f'<div class="task">- {task} [pending]</div>'
    
    return render_template_string(HTML_TEMPLATE + """
        <h2>All Tasks</h2>
        <div class="task-list">
            {{ tasks|safe }}
        </div>
        <br>
        <a href="{{ url_for('mark_done') }}">Mark Task as Done</a>
    """, tasks=tasks_html)

@app.route('/mark-done', methods=['GET', 'POST'])
def mark_done():
    if request.method == 'POST':
        day = request.form['day']
        task_title = request.form['task_title']
        markDone(day, task_title)
        return redirect(url_for('show_tasks'))
    
    return render_template_string(HTML_TEMPLATE + """
        <h2>Mark Task as Done</h2>
        <form method="POST">
            <label for="day">Day (e.g., Monday):</label><br>
            <input type="text" id="day" name="day" required style="width: 100%; padding: 8px;"><br><br>
            <label for="task_title">Task Title:</label><br>
            <input type="text" id="task_title" name="task_title" required style="width: 100%; padding: 8px;"><br><br>
            <input type="submit" value="Mark as Done">
        </form>
    """)

@app.route('/summary')
def show_summary():
    summary = showSummary(return_string=True)
    return render_template_string(HTML_TEMPLATE + """
        <h2>Summary</h2>
        <pre>{{ summary }}</pre>
    """, summary=summary)


if __name__ == '__main__':
    app.run(debug=True)