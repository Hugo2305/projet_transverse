import math

GRAVITY = 9.81

def compute_trajectory(x0, y0, angle_deg, speed, t):
    angle_rad = math.radians(angle_deg)
    x = x0 + speed * math.cos(angle_rad) * t
    y = y0 - (speed * math.sin(angle_rad) * t - 0.5 * GRAVITY * t**2)
    return x, y

def get_trajectory_points(x0, y0, angle, speed, steps=50):
    points = []
    for i in range(steps):
        t = i * 0.1
        x, y = compute_trajectory(x0, y0, angle, speed, t)
        if y > 600:
            break
        points.append((x, y))
    return points
