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

    2. DAILY SCHEDULE (6AM-11PM):
    - Assign time blocks to tasks and make sure the allocated time is enough for the activity
    - No tasks between 10AM-5PM (work hours)

    CRITICAL RULES:
    1. Use ONLY valid JSON syntax
    2. Use double quotes for all keys and values EXCEPT contractions (you're, don't, etc.)
    3. Absolutely NO trailing commas
    4. NO markdown formatting (no ```json ```)
    5. NO additional text outside the JSON object
    6. All time slots must be in 24-hour format (e.g., "17:00")
    8. Escape ALL apostrophes in text with a backslash (e.g., "children\'s story")
    9. NEVER use straight double quotes within text strings - use single quotes instead
    10. Example of properly escaped text: "Read a short children\'s story"
    11. Avoid putting unnecessary tasks like grocery shopping and any others, just put in tasks that conform to my goals
    12. All times in 24-hour format (e.g., "17:00")
    14. Balance mental/physical activities
    15. Progressive difficulty throughout week
    16. Weekend schedules should be more flexible
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


