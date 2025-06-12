import google.generativeai as genai
import json
import re

API_KEY = "AIzaSyDUiR0PPoQ6syLln02ivXmsKswFwX2weqY"
genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash")  

def generateSchedule(goal):
    prompt = """Create a weekly schedule with these requirements:

    1. WEEKLY TASKS:
    - Generate 1-6 specific tasks/goals for each weekday
    - Example format: ["Review German vocabulary", "Complete grammar exercises"]

    2. DAILY SCHEDULE (5AM-11PM):
    - Assign time blocks to tasks
    - No tasks between 10AM-5PM (work hours)
    - Must include:
    * Wake up time
    * Breakfast, lunch, dinner
    * Short breaks
    * Wind-down time before sleep

    STRICT OUTPUT FORMAT (RAW JSON ONLY):
    {
        "weekly_tasks": {
            "Monday": ["Task 1", "Task 2"],
            "Tuesday": ["Task 1", "Task 2"]
        },
        "daily_schedule": {
            "Monday": {
                "05:00": "Wake up",
                "06:00": "Task 1",
                "07:00": "Breakfast"
            },
            "Tuesday": {
                "05:00": "Wake up",
                "06:00": "Task 1",
                "07:00": "Breakfast"
            }
        }
    }

    CRITICAL RULES:
    1. Use ONLY valid JSON syntax
    2. Use double quotes for all keys and values EXCEPT contractions (you're, don't, etc.)
    3. Absolutely NO trailing commas
    4. NO markdown formatting (no ```json ```)
    5. NO additional text outside the JSON object
    6. All time slots must be in 24-hour format (e.g., "17:00")
    7. Work hours (10:00-17:00) must contain only "Work" as activity

    EXAMPLE OF VALID CONTRACTIONS:
    - "Review children's stories"
    - "Practice you're/your differences"
    - "Don't forget breaks"
    """

    try:
        response = model.generate_content(
            prompt,
            generation_config={
                "temperature": 0.3,  
                "max_output_tokens": 2000,
                "response_mime_type": "application/json"  
            }
        )
        
        content = response.text.strip()

        json_match = re.search(r"\{.*\}", content, re.DOTALL)
        if not json_match:
            print("No JSON object found in response.")
            print(f"Raw response:\n{content}")
            return None
        json_str = json_match.group(0)

        json_str = json_str.replace("'", '"')  
        json_str = re.sub(r",\s*}", "}", json_str)  
        json_str = re.sub(r",\s*]", "]", json_str)  

        try:
            schedule = json.loads(json_str)
        except json.JSONDecodeError as e:
            print(f"JSON parsing failed. Error: {e}")
            print(f"Problematic content was:\n{json_str}")
            return None

        required_keys = {"weekly_tasks", "daily_schedule"}
        if not all(key in schedule for key in required_keys):
            raise ValueError("Missing required keys in response")

        return schedule
        
    except json.JSONDecodeError as e:
        print(f"JSON parsing failed. Error: {e}")
        print(f"Problematic content was:\n{content}")
        return None
    except Exception as e:
        print(f"Error generating schedule: {e}")
        return None

def saveSChedule(schedule):
    if not schedule:
        print("No schedule to save")
        return
        
    try:
        with open("data/schedule.json", "w") as f:
            json.dump(schedule, f, indent=4)
            print("Schedule saved successfully")
    except Exception as e:
        print(f"Error saving schedule: {e}")