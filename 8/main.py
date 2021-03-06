#!/usr/bin/python3
import os
from datetime import datetime

def get_entry(line):
    l = line[1:]
    date_time, action = l.split("]")
    
    date, time = date_time.split(" ")
    year, month, day = date.split("-")
    hour, minute = time.split(":")
    d = datetime(int(year), int(month), int(day), int(hour), int(minute))

    a = None
    g = None
    action = action[1:-1]
    if action == "falls asleep":
        a = "f"
    elif action == "wakes up":
        a = "w"
    else:
        a = "g"
        g = action.split(" ")[1][1:]

    return {
        "date_time": d,
        "action": a,
        "guard" : g
    }

def main():

    entries = []

    with open(os.path.dirname(__file__) + "/data") as f:
        for line in f:
            entries.append(get_entry(line))

    entries.sort(key=lambda x: x["date_time"])
    
    guard_sleeps = {}

    actual_guard = None
    sleep_start = None

    for e in entries:
        if e["action"] == "g":
            actual_guard = e["guard"]
        elif e["action"] == "f":
            sleep_start = e["date_time"]
        else:
            sleep_time = e["date_time"] - sleep_start
            if actual_guard in guard_sleeps:
                guard_sleeps[actual_guard]["time"] += sleep_time.total_seconds()
                
                for i in range(sleep_start.minute, e["date_time"].minute):
                    guard_sleeps[actual_guard]["dist"][i] += 1

            else:
                guard_sleeps[actual_guard] = {
                    "time": sleep_time.total_seconds(),
                    "dist": [0 for _ in range(0,60)]
                }
                for i in range(sleep_start.minute, e["date_time"].minute):
                    guard_sleeps[actual_guard]["dist"][i] += 1

            sleep_start = None


    max_m = 0
    minute = 0
    guard = None

    for k, v in guard_sleeps.iteritems():
        for i in range(0, 60):
            if v["dist"][i] > max_m:
                max_m = v["dist"][i]
                minute = i
                guard = k

    print guard, minute, max_m

    return 0
                

if __name__ == "__main__":
    main()