"""Run the motor/PID simulation and plot its sampled speed."""

import argparse
import math
from pathlib import Path

if __package__:
    from .pid import PID
    from .motor import Motor
else:
    from pid import PID
    from motor import Motor


def simulate(kp=1.0, ki=0.2, kd=0.05):
    pid = PID(kp=kp, ki=ki, kd=kd)
    motor = Motor()
    target_speed = 100
    dt = 0.01

    # Include the initial state, then record every post-update sample.
    times = [0.0]
    speeds = [motor.speed]
    for i in range(500):
        control = pid.update(target_speed, motor.speed, dt)
        speed = motor.update(control, dt)
        if not math.isfinite(speed):
            raise ValueError("Simulation diverged; try smaller PID gains.")
        times.append((i + 1) * dt)
        speeds.append(speed)

        if i % 50 == 0:
            print(f"time={times[-1]:.2f}s, speed={speed:.2f}")

    return times, speeds, target_speed


def plot_response(times, speeds, target_speed):
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots()
    ax.plot(times, speeds, label="Motor speed")
    ax.axhline(target_speed, color="tab:red", linestyle="--", label="Target speed")
    ax.set(xlabel="Time (s)", ylabel="Speed (model units)", title="PID motor simulation")
    ax.grid(True, alpha=0.3)
    ax.legend()
    fig.tight_layout()
    return fig


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--kp", type=float, default=1.0)
    parser.add_argument("--ki", type=float, default=0.2)
    parser.add_argument("--kd", type=float, default=0.05)
    parser.add_argument("--no-show", action="store_true", help="Save without opening a GUI window")
    parser.add_argument("--save", type=Path, default=Path(__file__).with_name("pid_response.png"),
                        help="Output image path (default: simulation/pid_response.png)")
    args = parser.parse_args()
    if not all(math.isfinite(gain) for gain in (args.kp, args.ki, args.kd)):
        parser.error("PID gains must be finite numbers")

    # Select the non-GUI backend before importing pyplot for headless runs.
    if args.no_show:
        import matplotlib
        matplotlib.use("Agg")

    import matplotlib.pyplot as plt

    fig = plot_response(*simulate(args.kp, args.ki, args.kd))
    output = args.save.resolve()
    fig.savefig(output, dpi=150)
    print(f"Plot saved to: {output}")
    if not args.no_show:
        plt.show(block=True)
    plt.close(fig)


if __name__ == "__main__":
    main()
