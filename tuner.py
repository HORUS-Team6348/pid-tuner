from networktables import NetworkTables
from tabulate import tabulate

NetworkTables.initialize(server='localhost')
sd = NetworkTables.getTable("SmartDashboard")

error_history = []

def value_changed(key, value, isNew):
    if key == '/SmartDashboard/PID error':
        error_history.append((sd.getNumber("Timer", 0), value))

def find_max(array):
    max = -99999

    while True:
        time, error = array.pop(0)
        if error > max:
            max = error
        else:
            return (time, error)

def find_min(array):
    min = 99999

    while True:
        time, error = array.pop(0)
        if error < min:
            min = error
        else:
            return (time, error)


NetworkTables.addEntryListener(value_changed)

kP = float(input("Enter kP coefficient: "))

sd.putNumber("kP", kP)

input("Ready. When autonomous ends, press Enter to continue")

periods = []

while error_history:
    try:
        time_first, err_first = find_max(error_history)
        time_min, err_min = find_min(error_history)
        time_second, err_second = find_max(error_history)
        periods.append((time_second-time_first, ))
    except IndexError:
        break

if len(periods) == 0:
    print("No periods detected: exiting")
elif len(periods) == 1:
    selected = 0
else:
    print("These are the detected periods: choose one")
    print(tabulate(periods, showindex=True, headers=["Index", "Period (seconds)"]))
    selected = int(input(f"Enter selection (0 - {len(periods)-1}): "))

Tu = periods[selected][0]

print(f"Final values for PI Ziegler-Nichols are: kP = {0.45*kP}, kI = {0.54 *(kP/Tu)}")

