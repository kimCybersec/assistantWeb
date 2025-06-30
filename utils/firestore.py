import os
import json
import base64
from firebase_admin import credentials, firestore, initialize_app
from datetime import datetime
from typing import Optional, Dict, Any

def initializeFirestore():
    credData = os.environ.get("GOOGLE_CREDENTIALS")
    
    if credData:
        try:
            decoded = base64.b64decode(credData).decode("utf-8")
            credJson = json.loads(decoded)
            cred = credentials.Certificate(credJson)
        except Exception as e:
            print(f"Error decoding credentials: {e}")
            cred = credentials.Certificate("schedulerFirebase.json")
    else:
        cred = credentials.Certificate("schedulerFirebase.json")
    
    try:
        initialize_app(cred)
        return firestore.client()
    except Exception as e:
        print(f"Error initializing Firestore: {e}")
        raise

db = initializeFirestore()

def saveSchedule(sessionId: str, scheduleData: Dict[str, Any]) -> bool:
    """Save complete schedule to Firestore"""
    if not scheduleData:
        print("No schedule data provided")
        return False

    try:
        scheduleRef = db.collection("userSchedules").document(sessionId)
        
        metadata = {
            '_meta': {
                'lastUpdated': datetime.utcnow().isoformat(),
                'created_at': scheduleData.get('_meta', {}).get('created_at', datetime.utcnow().isoformat()),
                'access_count': scheduleData.get('_meta', {}).get('access_count', 0) + 1
            }
        }
        
        scheduleRef.set({
            **scheduleData,
            **metadata
        }, merge=True)
        
        return True
    except Exception as e:
        print(f"Error saving schedule: {e}")
        return False

def getSchedule(sessionId: str) -> Optional[Dict[str, Any]]:
    """Retrieve complete schedule from Firestore"""
    try:
        docRef = db.collection("userSchedules").document(sessionId)
        doc = docRef.get()
        return doc.to_dict() if doc.exists else None
    except Exception as e:
        print(f"Error getting schedule: {e}")
        return None

def updateSchedule(sessionId: str, day: str, taskData: Dict[str, Any]) -> bool:
    """Update specific task in schedule"""
    if not day or not taskData:
        return False

    try:
        schedule_ref = db.collection("userSchedules").document(sessionId)
        
        schedule_ref.update({
            f"weeklyTasks.{day}": firestore.ArrayUnion([taskData]),
            "_meta.lastUpdated": datetime.utcnow().isoformat()
        })
        return True
    except Exception as e:
        print(f"Error updating task: {e}")
        return False

def updateTask(sessionId: str, day: str, taskTitle: str, status: str = "done") -> bool:
    """Update task status without creating duplicates"""
    try:
        scheduleRef = db.collection("userSchedules").document(sessionId)
        schedule = scheduleRef.get().to_dict() or {}
        
        updated = False
        weeklyTasks = schedule.get("weeklyTasks", {}).get(day, [])
        
        for i, task in enumerate(weeklyTasks):
            if isinstance(task, dict) and task.get("title") == taskTitle:
                weeklyTasks[i]["status"] = status
                updated = True
            elif isinstance(task, str) and task == taskTitle:
                weeklyTasks[i] = {"title": task, "status": status}
                updated = True
        
        if updated:
            scheduleRef.update({
                f"weeklyTasks.{day}": weeklyTasks,
                "_meta.last_updated": datetime.utcnow().isoformat()
            })
            return True
        return False
        
    except Exception as e:
        print(f"Error updating task status: {e}")
        return False
