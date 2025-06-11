import google.generativeai as genai
import json
import re

API_KEY = "AIzaSyDUiR0PPoQ6syLln02ivXmsKswFwX2weqY"
genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash")  # Updated to newer model

def generateSchedule(goal):
    prompt = f"""You are a weekly schedule and planning assistant. Based on the user's goal:
    "{goal}"
    Create a weekly schedule in valid JSON format with exactly this structure:
    {{
        "Monday": ["Task 1", "Task 2"],
        "Tuesday": ["Task 1", "Task 2"],
        "Wednesday": ["Task 1", "Task 2"],
        "Thursday": ["Task 1", "Task 2"],
        "Friday": ["Task 1", "Task 2"],
        "Saturday": ["Task 1", "Task 2"],
        "Sunday": ["Task 1", "Task 2"]
    }}
    Return ONLY the JSON object, with no additional text, explanations, or markdown formatting.
    """
    
    try:
        response = model.generate_content(
            prompt,
            generation_config={
                "temperature": 0.3,  # Less creative but more structured
                "max_output_tokens": 1000
            }
        )
        content = response.text
        
        # Clean the response to extract just the JSON
        json_match = re.search(r'\{[\s\S]*\}', content)
        if not json_match:
            raise ValueError("No JSON found in response")
            
        json_str = json_match.group(0)
        schedule = json.loads(json_str)
        
        # Validate the structure
        required_days = ["Monday", "Tuesday", "Wednesday", "Thursday", 
                        "Friday", "Saturday", "Sunday"]
        if not all(day in schedule for day in required_days):
            raise ValueError("Missing required days in schedule")
            
        return schedule
        
    except Exception as e:
        print(f"Error generating schedule: {e}")
        print("Raw response was:")
        print(content)
        return None

def saveSChedule(schedule):  # Fixed typo in function name
    if not schedule:
        print("No schedule to save")
        return
        
    try:
        with open("data/schedule.json", "w") as f:
            json.dump(schedule, f, indent=4)
            print("Schedule saved successfully")
    except Exception as e:
        print(f"Error saving schedule: {e}")