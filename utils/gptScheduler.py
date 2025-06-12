import google.generativeai as genai
import json
import re

API_KEY = "AIzaSyDUiR0PPoQ6syLln02ivXmsKswFwX2weqY"
genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash")

def generateSchedule(goal):
    prompt = f"""Create a weekly schedule with these requirements:

    1. WEEKLY TASKS:
    - 1-6 specific tasks per day
    - Example: ["Review vocabulary", "Complete exercises"]

    2. DAILY SCHEDULE (5AM-11PM):
    - No tasks between 10AM-5PM (work hours)
    - Include wake up, meals, breaks
    - Time blocks in 24-hour format

    Return ONLY this JSON format:
    {{
        "weekly_tasks": {{
            "Monday": ["Task 1", "Task 2"],
            "Tuesday": ["Task 1", "Task 2"]
        }},
        "daily_schedule": {{
            "Monday": {{
                "05:00": "Wake up",
                "06:00": "Task 1"
            }},
            "Tuesday": {{
                "05:00": "Wake up",
                "06:00": "Task 1"
            }}
        }}
    }}

    Rules:
    1. Use double quotes for JSON
    2. No trailing commas
    3. No markdown formatting
    4. No text outside JSON
    """

    try:
        response = model.generate_content(
            prompt,
            generation_config={
                "temperature": 0.3,
                "max_output_tokens": 2000,
                "response_type": "application/json"  # Updated parameter name
            }
        )
        
        # Extract and clean JSON
        content = response.text
        json_str = re.search(r'\{.*\}', content, re.DOTALL).group(0)
        
        # Fix common issues
        json_str = (json_str
            .replace("'", '"')
            .replace("True", "true").replace("False", "false")
        )
        json_str = re.sub(r',\s*([}\]])', r'\1', json_str)  # Remove trailing commas
        
        return json.loads(json_str)
        
    except Exception as e:
        print(f"Error generating schedule: {e}")
        print(f"Raw response was:\n{content}")
        return None

def saveSchedule(schedule):
    if not schedule:
        print("No schedule to save")
        return
        
    try:
        with open("data/schedule.json", "w") as f:
            json.dump(schedule, f, indent=4)
            print("Schedule saved successfully")
    except Exception as e:
        print(f"Error saving schedule: {e}")