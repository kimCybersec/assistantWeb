from .firestore import getSchedule, updateSchedule, updateTask, saveSchedule
from datetime import datetime

weekDays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

def loadSchedule(userId=None):
    """Load schedule from Firestore"""
    if not userId:
        return {day: [] for day in weekDays}
    
    scheduleData = getSchedule(userId)
    if not scheduleData:
        return {day: [] for day in weekDays}
    
    return scheduleData.get("weeklyTasks", {day: [] for day in weekDays})

def markDone(day: str, taskTitle: str, userId: str = None) -> bool:
    """Mark task as done without creating duplicates"""
    if userId:
        return updateTask(userId, day, taskTitle, "done")
    else:
        schedule = loadSchedule()
        if day not in schedule:
            return False
            
        updated = False
        for i, task in enumerate(schedule[day]):
            if isinstance(task, dict) and task.get("title") == taskTitle:
                schedule[day][i]["status"] = "done"
                updated = True
            elif isinstance(task, str) and task == taskTitle:
                schedule[day][i] = {"title": task, "status": "done"}
                updated = True
        
        if updated:
            saveSchedule(schedule)
            return True
        return False
    
def showSummary(userId=None, return_string=False):
    schedule = loadSchedule(userId)
    total = 0
    done = 0
    lines = []

    for day in weekDays:
        day_total = 0
        day_done = 0
        for task in schedule.get(day, []):
            day_total += 1
            if isinstance(task, dict) and task.get("status") == "done":
                day_done += 1
        total += day_total
        done += day_done
        lines.append(f"{day}: {day_done}/{day_total} tasks done")

    lines.append(f"\nOverall: {done}/{total} tasks completed ({total - done} pending)")
    summary = "\n".join(lines)
    return summary if return_string else print(summary)

def showAllTasks(userId=None):
    schedule = loadSchedule(userId)
    for day in weekDays:
        print(f"\n{day}:")
        for task in schedule.get(day, []):
            if isinstance(task, dict):
                status = task.get("status", "pending")
                print(f"  - {task.get('title', '')} [{status}]")
            else:
                print(f"  - {task} [pending]")