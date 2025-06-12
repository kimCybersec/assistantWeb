from flask import Flask, render_template_string, request, redirect, url_for
from utils.gptScheduler import generateSchedule, saveSChedule
from utils.tracker import showAllTasks, markDone, showSummary
import json

app = Flask(__name__)

# Neon dark theme template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Schedule Assistant</title>
    <style>
        body {
            font-family: 'Segoe UI', sans-serif;
            background: #0a0a0a;
            color: #00ffe5;
            padding: 30px;
            max-width: 900px;
            margin: auto;
        }
        h1, h2 {
            color: #00ffe5;
        }
        .menu a {
            margin-right: 15px;
            text-decoration: none;
            color: #00ffe5;
            font-weight: bold;
        }
        .menu {
            margin-bottom: 20px;
            border-bottom: 2px solid #00ffe5;
            padding-bottom: 10px;
        }
        .day-block {
            background: #121212;
            margin-bottom: 15px;
            border-left: 4px solid #00ffe5;
            border-radius: 6px;
            padding: 10px;
        }
        .day-btn {
            background: #00ffe5;
            color: #0a0a0a;
            font-weight: bold;
            padding: 10px;
            width: 100%;
            border: none;
            border-radius: 4px;
            margin-bottom: 10px;
            cursor: pointer;
        }
        .submit-btn {
            background-color: #00ffe5;
            color: #0a0a0a;
            padding: 12px;
            border: none;
            border-radius: 6px;
            font-weight: bold;
            cursor: pointer;
            margin-top: 15px;
        }
        ul {
            list-style-type: none;
            padding-left: 0;
        }
        li {
            margin-bottom: 8px;
        }
    </style>

    <script>
        function togglePopup(day) {
            const popup = document.getElementById(day + "-popup");
            popup.style.display = popup.style.display === "none" ? "block" : "none";
        }
    </script>
</head>
<body>
    <h1>Weekly Scheduler</h1>
    <div class="menu">
        <a href="{{ url_for('index') }}">Home</a> |
        <a href="{{ url_for('generate') }}">Generate Schedule</a> |
        <a href="{{ url_for('show_summary') }}">Summary</a>
    </div>

    {% block content %}{% endblock %}
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    data = json.load(open('data/schedule.json'))
    weekly = data.get("weekly_tasks", {})
    daily = data.get("daily_schedule", {})
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    if request.method == 'POST':
        for day in days:
            completed_tasks = request.form.getlist(day)
            for task in completed_tasks:
                markDone(day, task)
        return redirect(url_for('index'))

    content = """
    <form method="POST">
    <div class="days-container">
    """
    for day in days:
        tasks = weekly.get(day, [])
        schedule = daily.get(day, {})

        content += f"""
        <div class="day-block">
            <button type="button" class="day-btn" onclick="toggleDay('{day}')">{day}</button>
            <div id="{day}" class="day-content" style="display:none;">
                <h3>Tasks</h3>
                <ul>
        """
        if tasks:
            for task in tasks:
                task_title = task["title"] if isinstance(task, dict) else task
                status = task.get("status", "pending") if isinstance(task, dict) else "pending"
                checked = "checked" if status == "done" else ""
                style = "text-decoration: line-through; color: gray;" if status == "done" else ""
                content += f"""
                <li style="{style}">
                    <label>
                        <input type="checkbox" name="{day}" value="{task_title}" {checked}> {task_title}
                    </label>
                </li>
                """
        else:
            content += "<li>No tasks</li>"

        content += "</ul><h3>Schedule</h3><ul>"
        if schedule:
            for time, activity in schedule.items():
                content += f"<li><strong>{time}:</strong> {activity}</li>"
        else:
            content += "<li>No schedule</li>"

        content += "</ul></div></div>"

    content += """
    </div>
    <input type="submit" value="Update Tasks" class="submit-btn">
    </form>
    """

    return render_template_string(HTML_TEMPLATE + """
        {{ content|safe }}
        <script>
        function toggleDay(day) {
            var x = document.getElementById(day);
            x.style.display = (x.style.display === "none") ? "block" : "none";
        }
        </script>
    """, content=content)

@app.route('/generate', methods=['GET', 'POST'])
def generate():
    if request.method == 'POST':
        goal = request.form['goal']
        schedule = generateSchedule(goal)
        if schedule:
            saveSChedule(schedule)
            return redirect(url_for('index'))

    return render_template_string(HTML_TEMPLATE + """
        <h2>Generate Schedule</h2>
        <form method="POST">
            <label for="goal">What is your goal for this week?</label><br>
            <input type="text" id="goal" name="goal" required style="width: 100%; padding: 8px;"><br><br>
            <input type="submit" value="Generate Schedule">
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
