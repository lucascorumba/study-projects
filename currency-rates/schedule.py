from time import sleep
from datetime import datetime, timedelta
from sys import exit
import get_rates

# Inputs
fetches = int(input("Number of retrievals: "))

mult_h = input("Hours interval: ")
mult_min = input("Minutes interval: ")

t = datetime.now()
print(f"Current time: {t.time()}")

# Schedules one fetch right away and uses timedelta to define following ones
schedules = [t + timedelta(hours=i*int(mult_h), minutes=i*int(mult_min)) for i in range(fetches)]

print("Scheduled fetches: ")
for time in schedules:
    print(f"-> {time}")
    sleep(0.7)

res = input("Proceed? y/n ")
if res.lower() == "y":
    print("\nScheduled fetching started\n")
else:
    exit()

# Check queue for scheduled fetches
while schedules:
    try:
        now = datetime.now()
        if now > schedules[0]:
            print(f"===> Started process at {now.time()}\n")
            schedules.pop(0)
            rates = get_rates.runner("currency.db")
            print()
            get_rates.simple_report(rates)
            print()
        else:
            # 1800 sec -> 30 min | 2700 sec -> 45 min
            sleep_seconds = 2700
            print(f"Waiting for next trigger...\nTime now: {now.time()}\
            Next check: {now + timedelta(seconds=sleep_seconds)}\n")
            sleep(sleep_seconds)
    except IndexError:
        break
    
print("Fetch queue cleared")