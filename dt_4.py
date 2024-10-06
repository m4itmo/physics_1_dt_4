import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from random import random, randint

fps = 60


def speed_to_vector(magnitude, angle_deg):
    angle_rad = np.radians(angle_deg)
    return np.array([magnitude * np.cos(angle_rad), magnitude * np.sin(angle_rad)])


def protect_int(x: float) -> int:
    return 1 if x < 0 else int(x)


print('Select input mode:')
print('0 - random')
print('1 - manual')
mode = int(input('Mode: '))

width = (
    float(input('Enter the width of the container (e.g., 100): '))
) if mode == 1 else randint(50, 200)
height = (
    float(input(f'Enter the height of the container (e.g., {protect_int(width / 2)}): '))
) if mode == 1 else protect_int(width * random())

k = (width + height) / 150
m1 = (
    float(input(f'Enter the mass of the first body (e.g., {protect_int(k * 2)}): '))
) if mode == 1 else protect_int(k * 2)
m2 = (
    float(input(f'Enter the mass of the second body (e.g., {protect_int(k * 3)}): '))
) if mode == 1 else protect_int(k * 3)

v1_magnitude = (
    float(input(f'Enter the speed magnitude of the first body (e.g., {protect_int(k * 15)}): '))
) if mode == 1 else protect_int(k * 15)
v1_angle = (
    float(input(f'Enter the direction (angle in degrees) of the first body (e.g., {randint(0, 90)}): ')) % 360
) if mode == 1 else randint(0, 90)
v2_magnitude = (
    float(input(f'Enter the speed magnitude of the second body (e.g., {protect_int(k * 20)}): '))
) if mode == 1 else protect_int(k * 20)
v2_angle = (
    float(input(f'Enter the direction (angle in degrees) of the second body (e.g., {randint(90, 360)}): ')) % 360
) if mode == 1 else randint(90, 360)

v1 = speed_to_vector(v1_magnitude, v1_angle)
v2 = speed_to_vector(v2_magnitude, v2_angle)

pos1 = np.array([width * 0.25, height * 0.5])
pos2 = np.array([width * 0.75, height * 0.5])

r1 = min(width, height) / 10
r2 = r1 * 1.5
dt = 1 / fps


def update_positions():
    global pos1, pos2, v1, v2

    pos1 += v1 * dt
    pos2 += v2 * dt

    for pos, v, r in zip([pos1, pos2], [v1, v2], [r1, r2]):
        if pos[0] - r <= 0 or pos[0] + r >= width:
            v[0] *= -1
        if pos[1] - r <= 0 or pos[1] + r >= height:
            v[1] *= -1

    dist = np.linalg.norm(pos1 - pos2)
    if dist <= r1 + r2:
        resolve_collision()


def resolve_collision():
    global v1, v2

    n = (pos2 - pos1) / np.linalg.norm(pos2 - pos1)

    v1n = np.dot(v1, n)
    v2n = np.dot(v2, n)

    v1n_new = (v1n * (m1 - m2) + 2 * m2 * v2n) / (m1 + m2)
    v2n_new = (v2n * (m2 - m1) + 2 * m1 * v1n) / (m1 + m2)

    v1 += (v1n_new - v1n) * n
    v2 += (v2n_new - v2n) * n


fig, ax = plt.subplots()
ax.set_xlim(0, width)
ax.set_ylim(0, height)
ax.set_aspect('equal')
circle1 = plt.Circle(pos1, r1, fc='blue')
circle2 = plt.Circle(pos2, r2, fc='red')
ax.add_patch(circle1)
ax.add_patch(circle2)


def animate(i):
    update_positions()
    circle1.set_center(pos1)
    circle2.set_center(pos2)
    return circle1, circle2


ani = FuncAnimation(fig, animate, frames=500, interval=10, blit=True)
plt.show()
