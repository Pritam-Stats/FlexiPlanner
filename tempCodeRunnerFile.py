from datetime import datetime, timedelta


class ScheduleGenerator:
    def __init__(self, wakeup_time):
        self.wakeup_time = wakeup_time
        self.schedule = []
        self.deep



# Example usage
if __name__ == "__main__":
    input_time = input("Enter wake-up time (HH:MM AM/PM): ")
    while True:
        try:
            wakeup_time = datetime.strptime(input_time, "%I:%M %p")
            generator = ScheduleGenerator(wakeup_time)
            schedule = generator.generate_schedule()

            print("\nYour Customized Schedule:")
            for task in schedule:
                print(f"{task['start']} - {task['end']}: {task['task']}")
            break  # Exit the loop once valid input is provided
        except ValueError:
            print("Invalid time format. Please enter time as HH:MM AM/PM.")
            input_time = input("Enter wake-up time (HH:MM AM/PM): ")


