from utils.gptScheduler import generateSchedule
from utils.tracker import showAllTasks, markDone, showSummary
from utils.firestore import saveSchedule, getSchedule

def main():
    print("""
    Weekly scheduler and task tracker
    1. Generate schedule with GPT
    2. Show all tasks
    3. Mark task as done
    4. Show summary
    5. Exit
    """)

def run():
    userId = "cli_user"  # Default user ID for CLI
    
    while True:
        main()
        choice = input("Enter your choice (1-5): ")
        
        if choice == "1":
            userGoal = input("What is your goal for this week? ")
            schedule = generateSchedule(userGoal, sessionId=userId)
        
        elif choice == "2":
            showAllTasks(userId=userId)
        
        elif choice == "3":
            day = input("Enter the day (e.g., Monday): ")
            taskTitle = input("Enter the task title to mark as done: ")
            markDone(day, taskTitle, userId=userId)
        
        elif choice == "4":
            showSummary(userId=userId)
        
        elif choice == "5":
            print("Exiting the program.")
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    run()