# import firebase_admin
# from firebase_admin import credentials, firestore
# import os

# # Initialize Firestore
# def initializeFirestore():
#     if not firebase_admin._apps:
#         # Use environment variable or path to your service account key
#         cred_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "serviceAccountKey.json")
#         cred = credentials.Certificate(cred_path)
#         firebase_admin.initialize_app(cred)
    
#     return firestore.client()

# db = initializeFirestore()

# def getSchedule():
#     doc_ref = db.collection("schedules").document("current")
#     doc = doc_ref.get()
#     if doc.exists:
#         return doc.to_dict()
#     return {
#         "weekly_tasks": {},
#         "daily_schedule": {}
#     }

# def saveSchedule(schedule):
#     db.collection("schedules").document("current").set(schedule)

# def markTaskDone(day, task_title):
#     schedule = getSchedule()
#     weekly_tasks = schedule.get("weekly_tasks", {})
    
#     if day not in weekly_tasks:
#         return False
    
#     updated_tasks = []
#     for task in weekly_tasks[day]:
#         if isinstance(task, dict) and task.get("title") == task_title:
#             task["status"] = "done"
#             updated_tasks.append(task)
#         elif isinstance(task, str) and task == task_title:
#             updated_tasks.append({"title": task, "status": "done"})
#         else:
#             updated_tasks.append(task)
    
#     weekly_tasks[day] = updated_tasks
#     schedule["weekly_tasks"] = weekly_tasks
#     saveSchedule(schedule)
#     return True