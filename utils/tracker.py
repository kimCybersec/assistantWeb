import json
import os

dataFile = "data/schedule.json"
weekDays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

def checkSchedule():
    if not os.path.exists("data"):
        os.makedirs("data")
    if not os.path.exists(dataFile):
        with open(dataFile, "w") as f:
            json.dump({day: [] for day in weekDays}, f, indent=4)

def loadSchedule():
    checkSchedule()
    with open(dataFile, "r") as f:
        try:
            data = json.load(f)
            if not isinstance(data, dict):
                return {day: [] for day in weekDays}
            return data
        except json.JSONDecodeError:
            return {day: [] for day in weekDays}

def saveSchedule(schedule):
    with open(dataFile, "w") as f:
        json.dump(schedule, f, indent=4)

def markDone(day, taskTitle):
    schedule = loadSchedule()
    if day not in schedule:
        print(f"'{day}' is not a valid weekday in the schedule.")
        return
    for i, task in enumerate(schedule[day]):
        if isinstance(task, dict) and task.get("title") == taskTitle:
            task["status"] = "done"
        elif isinstance(task, str) and task == taskTitle:
            schedule[day][i] = {"title": task, "status": "done"}
    saveSchedule(schedule)

def showSummary(return_string=False):
    schedule = loadSchedule()
    total = 0
    done = 0
    for day in weekDays:
        for task in schedule.get(day, []):
            if isinstance(task, dict):
                total += 1
                if task.get("status") == "done":
                    done += 1
            elif isinstance(task, str):
                total += 1
    summary = f"Total tasks: {total}, Done: {done}, Pending: {total - done}"
    return summary if return_string else print(summary)

def showAllTasks():
    schedule = loadSchedule()
    for day in weekDays:
        print(f"\n{day}:")
        for task in schedule.get(day, []):
            if isinstance(task, dict):
                status = task.get("status", "pending")
                print(f"  - {task.get('title', '')} [{status}]")
            elif isinstance(task, str):
                print(f"  - {task} [pending]")
                

if __name__ == "__main__":
    showAllTasks()
    showSummary()
    markDone("Monday", "Task 1")
