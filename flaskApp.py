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
<style>
    body {
        font-family: 'Segoe UI', sans-serif;
        background: #f9f9f9;
        color: #333;
        padding: 30px;
        max-width: 800px;
        margin: auto;
    }
    h1, h2 {
        color: #4b2e83;
    }
    .menu a {
        margin-right: 15px;
        text-decoration: none;
        color: #4b2e83;
        font-weight: bold;
    }
    .menu {
        margin-bottom: 20px;
        border-bottom: 2px solid #ddd;
        padding-bottom: 10px;
    }
    .task-list {
        background: #fff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    .task {
        padding: 8px;
        margin-bottom: 5px;
        border-left: 5px solid #ccc;
    }
    .done {
        color: #999;
        text-decoration: line-through;
        border-color: #4caf50;
    }
    form input[type="text"], form input[type="submit"] {
        width: 100%;
        padding: 10px;
        margin-top: 10px;
        border-radius: 6px;
        border: 1px solid #ccc;
    }
    form input[type="submit"] {
        background-color: #4b2e83;
        color: white;
        cursor: pointer;
    }
</style>

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
    data = json.load(open('data/schedule.json'))
    weekly = data.get("weekly_tasks", {})
    daily = data.get("daily_schedule", {})

    tasks_html = "<h2>Weekly Task List</h2><div class='task-list'>"
    for day, tasks in weekly.items():
        tasks_html += f"<h3>{day}</h3>"
        for task in tasks:
            tasks_html += f"<div class='task'>- {task}</div>"
    tasks_html += "</div>"

    schedule_html = "<h2>Daily Schedule</h2><div class='task-list'>"
    for day, slots in daily.items():
        schedule_html += f"<h3>{day}</h3>"
        for time, activity in slots.items():
            schedule_html += f"<div class='task'><strong>{time}</strong>: {activity}</div>"
    schedule_html += "</div>"

    return render_template_string(HTML_TEMPLATE + """
        {{ tasks|safe }}
        {{ schedule|safe }}
        <br>
        <a href="{{ url_for('mark_done') }}">Mark Task as Done</a>
    """, tasks=tasks_html, schedule=schedule_html)


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