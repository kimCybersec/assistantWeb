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
    - Example format: ["Review German vocabulary","Read a short German children's story", "Complete grammar exercises"]

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
    1. Use ONLY valid JSON syntax
    2. Use double quotes for all keys and values EXCEPT contractions (you're, don't, etc.)
    3. Absolutely NO trailing commas
    4. NO markdown formatting (no ```json ```)
    5. NO additional text outside the JSON object
    6. All time slots must be in 24-hour format (e.g., "17:00")
    7. Work hours (10:00-17:00) must contain only "Work" as activity
    8. Escape ALL apostrophes in text with a backslash (e.g., "children\'s story")
    9. NEVER use straight double quotes within text strings - use single quotes instead
    10. Example of properly escaped text: "Read a short German children\'s story"
    11. Avoid using " instead of ' for example( "you"re" should be "you're")

    EXAMPLE OF VALID CONTRACTIONS:
    - "Review children's stories"
    - "Practice you're/your differences"
    - "Don't forget breaks"
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


