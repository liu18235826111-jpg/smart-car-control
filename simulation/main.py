from pid import PID
from motor import Motor

pid = PID(kp=1.0, ki=0.2, kd=0.05)
motor = Motor()

target_speed = 100
dt = 0.01

for i in range(500):
    control = pid.update(target_speed, motor.speed, dt)
    speed = motor.update(control, dt)

    if i % 50 == 0:
        print(f"time={i * dt:.2f}s, speed={speed:.2f}")