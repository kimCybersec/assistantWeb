from flask import Flask, render_template, request, redirect, url_for, jsonify
from utils.gptScheduler import generateSchedule
from utils.firestore import saveSchedule, getSchedule, updateSchedule, updateTask
from utils.userManager import generateUserId
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "dev-secret-key")

@app.before_request
def beforeRequest():
    """Generate user ID for each request"""
    request.userId = generateUserId()

@app.route('/', methods=['GET', 'POST'])
def index():
    scheduleData = getSchedule(request.userId) or {
        "weeklyTasks": {},
        "dailySchedule": {}
    }
    
    if request.method == 'POST':
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        for day in days:
            completedTasks = request.form.getlist(f"task_{day}")
            for taskTitle in completedTasks:
                updateTask(
                    request.userId,
                    day,
                    {
                        "title": taskTitle,
                        "status": "done",
                        "completedAt": datetime.utcnow().isoformat()
                    }
                )
        return redirect(url_for('index'))

    return render_template('index.html', 
                         scheduleData=scheduleData,
                         days=["Monday", "Tuesday", "Wednesday", "Thursday", 
                               "Friday", "Saturday", "Sunday"])

@app.route('/generate', methods=['GET', 'POST'])
def generateScheduleRoute():
    if request.method == 'POST':
        goal = request.form.get('goal')
        if goal:
            schedule = generateSchedule(goal, request.userId)
            if schedule:
                return redirect(url_for('index'))
    
    return render_template('generate.html')

@app.route('/summary')
def getSummary():
    scheduleData = getSchedule(request.userId) or {"weeklyTasks": {}}
    weeklyTasks = scheduleData.get("weeklyTasks", {})
    
    summary = []
    total = completed = 0
    
    for day, tasks in weeklyTasks.items():
        day_total = len(tasks)
        day_completed = sum(1 for t in tasks if isinstance(t, dict) and t.get("status") == "done")
        total += day_total
        completed += day_completed
        summary.append(f"{day}: {day_completed}/{day_total} tasks completed")
    
    summary.append(f"\nOverall: {completed}/{total} tasks completed")
    
    return render_template('summary.html', summary="\n".join(summary))

@app.route('/update-task', methods=['POST'])
def updateTaskRoute():
    try:
        data = request.get_json()
        day = data.get('day')
        taskTitle = data.get('taskTitle')
        status = data.get('status')
        userId = request.userId
        
        if not all([day, taskTitle, status]):
            return jsonify({'success': False, 'error': 'Missing parameters'}), 400
        
        updateTask(userId, day, taskTitle, status)
        
        return jsonify({'success': True})
    except Exception as e:
        print(f"Error updating task: {e}")
        return jsonify({'success': False}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 50000)))