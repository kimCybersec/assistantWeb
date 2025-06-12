import json
import os

dataFile = "data/schedule.json"
weekDays = ['Monday', "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

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
            weekly_tasks = data.get("weekly_tasks", {})
            return {day: weekly_tasks.get(day, []) for day in weekDays}
        except json.JSONDecodeError:
            return {day: [] for day in weekDays}


def saveSchedule(schedule):
    with open(dataFile, "r") as f:
        data = json.load(f)
    data["weekly_tasks"] = schedule
    with open(dataFile, "w") as f:
        json.dump(data, f, indent=4)


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
    lines = []

    for day in weekDays:
        day_total = 0
        day_done = 0
        for task in schedule.get(day, []):
            if isinstance(task, dict):
                day_total += 1
                if task.get("status") == "done":
                    day_done += 1
            elif isinstance(task, str):
                day_total += 1
        total += day_total
        done += day_done
        lines.append(f"{day}: {day_done}/{day_total} tasks done")

    lines.append(f"\nOverall: {done}/{total} tasks completed ({total - done} pending)")
    summary = "\n".join(lines)
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
