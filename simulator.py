from networktables import NetworkTables
import time
import math

NetworkTables.initialize()
sd = NetworkTables.getTable("SmartDashboard")

sd.putNumber("Timer", 0)

a = input("Click Enter to begin simulation")

kP = sd.getNumber("kP", 1)

start = time.monotonic()
current = time.monotonic() - start

while current< 10:
    current = time.monotonic() - start
    error     = math.sin(kP*current)

    print(f"{current}: {error}")

    sd.putNumber("Timer", current)
    sd.putNumber("PID error", error)


print(sd)