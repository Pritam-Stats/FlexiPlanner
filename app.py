from flask import Flask, render_template, request
from datetime import datetime, timedelta

app = Flask(__name__)

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



# Schedule generator class
# class ScheduleGenerator:
#     def __init__(self, wakeup_time):
#         self.wakeup_time = wakeup_time


#     def determine_block(self):
#         # Constraints and time blocks
#         constraints = [
#             {"start": "00:00", "end": "07:00", "message": "Night Mode: Focused study in the Hall room."},
#             {"start": "07:00", "end": "10:00", "message": "Early Morning Block: Use Hall room. Light tasks, no tea until 9 AM."},
#             {"start": "10:00", "end": "12:00", "message": "Morning Block: Use Study room, deep work for 2 hours."},
#             {"start": "12:00", "end": "14:00", "message": "Midday Break: Relax, have lunch after 1 PM."},
#             {"start": "14:00", "end": "19:00", "message": "Afternoon Block: Use study room for deep work sessions."},
#             {"start": "19:00", "end": "23:00", "message": "Evening Block: Relax or do light tasks. Study room unavailable."},
#             {"start": "23:00", "end": "00:00", "message": "Late Night Block: Use hall room for focused study or planning."},
#         ]

#         # Convert wake-up time to minutes since midnight
#         wakeup_minutes = self.wakeup_time.hour * 60 + self.wakeup_time.minute

#         # Helper function to convert time string to minutes
#         def time_to_minutes(time_str):
#             time_obj = datetime.strptime(time_str, "%H:%M")
#             return time_obj.hour * 60 + time_obj.minute

#         # Determine the block
#         for constraint in constraints:
#             start_minutes = time_to_minutes(constraint["start"])
#             end_minutes = time_to_minutes(constraint["end"])
            
#             if start_minutes <= wakeup_minutes < end_minutes:
#                 return constraint["message"]

#         return "Error: Time not within constraints."


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        time_input = request.form.get("time_input")
        try:
            wakeup_time = datetime.strptime(time_input, "%H:%M")
            schedule = ScheduleGenerator(wakeup_time).determine_block()
            return render_template("schedule.html", wakeup_time=time_input, schedule=schedule)
        except ValueError:
            return render_template("index.html", error="Invalid time format. Please try again.")
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
