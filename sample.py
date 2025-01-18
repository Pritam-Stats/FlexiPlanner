from datetime import datetime, timedelta

class ScheduleGenerator:
    def __init__(self, wakeup_time):
        self.wakeup_time = wakeup_time
        self.schedule = []
        self.deep_work_completed = 0
        self.light_work_completed = 0
        
    def add_activity(self, start_time, duration: int, activity, location=""):
        """ To add every activity, starting from the wake up time,
            start_time = time (H:M)
            duration = int (Minutes)
            activity = task (text)
            location : Optional (default: None)"""
        
        end_time = (datetime.strptime(start_time, "%H:%M") + timedelta(minutes=duration)).strftime("%H:%M")
        location_str = f" ({location})" if location else ""
        self.schedule.append(f"{start_time}-{end_time}: {activity}{location_str}")
        return end_time

    def is_study_room_time(self, time_str):
        time = datetime.strptime(time_str, "%H:%M")
        study_start = datetime.strptime("09:00", "%H:%M")
        study_end = datetime.strptime("19:00", "%H:%M")
        return (study_start.time() <= time.time() < study_end.time())

    def can_take_bath(self, time_str):
        time = datetime.strptime(time_str, "%H:%M")
        no_bath_start = datetime.strptime("09:00", "%H:%M")
        no_bath_end = datetime.strptime("12:00", "%H:%M")
        return not (no_bath_start.time() <= time.time() < no_bath_end.time())
    
    def can_have_TeaCoffee(self, time_str):
        time = datetime.strptime(time_str, "%H:%M")
        no_coffee_start = datetime.strptime("01:00", "%H:%M")
        no_coffee_end = datetime.strptime("09:00", "%H:%M")
        return not (no_coffee_start.time() <= time.time() < no_coffee_end.time())
    
    def is_Unproductive(self, time_str):
        time = datetime.strptime(time_str, "%H:%M")
        unproductive_start = datetime.strptime("18:30", "%H:%M")
        unproductive_end = datetime.strptime("23:00", "%H:%M")
        return (unproductive_start.time() <= time.time() < unproductive_end.time())

    def determine_block(self):
        current_time = self.wakeup_time.strftime("%H:%M")
        
        # Morning routine
        if self.can_take_bath(current_time):
            current_time = self.add_activity(current_time, 60, "Get up and Take Bath. Complete morning routine.")
        else:
            current_time = self.add_activity(current_time, 20, "Fresh up")

        # First tea/coffee
        if self.can_have_TeaCoffee(current_time):
            current_time = self.add_activity(current_time, 20, "Tea/Coffee")

        # Morning planning
        current_time = self.add_activity(current_time, 20, "Plan the day and Setup the Space")

        while (self.deep_work_completed < 360 or self.light_work_completed < 120):
            # Check for end of day
            # if datetime.strptime(current_time, "%H:%M") >= datetime.strptime("23:00", "%H:%M"):
            #     break
                
            # Determine location
            location = "Study Room" if self.is_study_room_time(current_time) else "Hall Room"

            # Check for meal times first
            current_time_obj = datetime.strptime(current_time, "%H:%M")
            if "12:30" <= current_time <= "14:00" and current_time_obj.time() < datetime.strptime("14:00", "%H:%M").time():
                current_time = self.add_activity(current_time, 45, "Lunch Break")
                continue
            elif "16:00" <= current_time <= "16:30":
                current_time = self.add_activity(current_time, 20, "Evening Tea")
                continue
            elif "22:15" <= current_time <= "23:00":
                current_time = self.add_activity(current_time, 45, "Dinner")
                continue

            # Handle unproductive time
            if self.is_Unproductive(current_time):
                if current_time < "19:00":
                    current_time = self.add_activity(current_time, 40, "Exercise time: walk or cycling")
                elif current_time < "20:30":
                    current_time = self.add_activity(current_time, 60, "Light activities or relaxation")
                elif current_time < "21:30":
                    current_time = self.add_activity(current_time, 60, "Complete Dinner by 10:30 PM")
                else:
                    current_time = self.add_activity(current_time, 30, "Brain Dumping routine")
                    continue

            # Deep work blocks
            if self.deep_work_completed < 360:
                current_time = self.add_activity(current_time, 120, "Deep Work Session", location)
                self.deep_work_completed += 120
                current_time = self.add_activity(current_time, 30, "Break - Walk around, stretch, water")
            
            # Light work blocks
            elif self.light_work_completed < 120:
                current_time = self.add_activity(current_time, 60, "Light Work Session (If energy remains.)", location)
                self.light_work_completed += 60
                current_time = self.add_activity(current_time, 20, "Take a Quick Break")

        return self.schedule

def main():
    print("Welcome to Schedule Generator!")
    print("This will create a schedule based on your wake-up time.")
    time_input = input("Enter wake up time (HH:MM AM/PM): ")
    try:
        wakeup_time = datetime.strptime(time_input, "%I:%M %p")
        scheduler = ScheduleGenerator(wakeup_time)
        schedule = scheduler.determine_block()
        
        print("\nHere is your Personalized Schedule:")
        print("=" * 50)
        for item in schedule:
            print(item)
            
    except ValueError:
        print("Invalid time format. Please use HH:MM AM/PM (e.g., 06:30 AM)")

if __name__ == "__main__":
    main()