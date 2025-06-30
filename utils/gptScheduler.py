import google.generativeai as genai
import json
import re
import os
from .firestore import saveSchedule

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


def generateSchedule(goal, sessionId = "anonymous"):
    prompt = f"""Create a weekly schedule with this goal: "{goal}"

    Requirements:

    1. WEEKLY TASKS:
    - Generate 1-6 specific tasks/goals for each weekday
    - Example format: ["Do this task","Do that task", "Do that other task"]

    2. DAILY SCHEDULE (5AM-11PM):
    - Assign time blocks to tasks
    - No tasks between 10AM-5PM (work hours)
    - Must include:
    * Wake up time
    * Breakfast, lunch, dinner
    * Short breaks
    * Wind-down time before sleep

    STRICT OUTPUT FORMAT (RAW JSON ONLY):
    {{
        "weeklyTasks": {{
            "Monday": ["Task 1", "Task 2"],
            "Tuesday": ["Task 1", "Task 2"]
        }},
        "dailySchedule": {{
            "Monday": {{
                "05:00": "Wake up",
                "06:00": "Task 1",
                "07:00": "Breakfast"
            }},
            "Tuesday": {{
                "05:00": "Wake up",
                "06:00": "Task 1",
                "07:00": "Breakfast"
            }}
        }}
    }}

    CRITICAL RULES:
    1. Never schedule tasks during 9:00-17:00 except "Work"
    2. All times in 24-hour format (e.g., "17:00")
    3. Include transition time between activities
    4. Balance mental/physical activities
    5. Progressive difficulty throughout week
    6. Weekend schedules should be more flexible
    7. Account for 15-minute buffer between major activities

    """

    model = genai.GenerativeModel("gemini-1.5-flash")  
    try:
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=2.0,  
                max_output_tokens=2000,
            )
        )
        
        content = response.text.strip()
        scheduleData = json.loads(content)
        
        saveSchedule(sessionId, scheduleData)
        return scheduleData
        
    except json.JSONDecodeError as e:
        print(f"JSON parsing failed. Error: {e}")
        print(f"Problematic content was:\n{content}")
        return None
    except Exception as e:
        print(f"Error generating schedule: {e}")
        return None


