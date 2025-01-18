from datetime import datetime, timedelta

def is_Unproductive(start_time, end_time):
    time_start = datetime.strptime(start_time, "%H:%M")
    time_end = datetime.strptime(end_time, "%H:%M")
    unproductive_time_start = datetime.strptime("18:30", "%H:%M")
    unproductive_time_end = datetime.strptime("23:00", "%H:%M")
    return (unproductive_time_start.time() < time_end.time() < unproductive_time_end.time() and unproductive_time_start.time() <= time_start.time() < unproductive_time_end.time())

print(is_Unproductive("16:50", "19:50"))