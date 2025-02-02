import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pandas as pd
from plan_mieszkania2 import salon, Kuchnia, Lazienka
from Ogrzewanie_z_wylaczaniem_grzejnikow1 import z_values
from Ogrzewanie_z_wylaczaniem_grzejnikow1 import load_temperature_data, update_temperature, calculate_door_means, update_door_temperatures, animate_heat_distribution


hx = 0.1
house = salon(-1, 1, -1, 0, hx)
kitchen = Kuchnia(0.2, 1, 0, 1, hx)
bathroom = Lazienka(-1, 0.2, 0, 1, hx)

bathroom.add_wall()
bathroom.add_door()
bathroom.add_radiator()
bathroom.add_window()

house.add_wall()
house.add_door()
house.add_window()
house.add_radiator()

kitchen.add_wall()
kitchen.add_window()
kitchen.add_door()
kitchen.add_radiator()

alpha = 0.025
hx = 0.2
ht = 0.01
dt = 0.01
S = 293
P = 2000
rho = 1.293
c = 1005
total_time = 0.6 * 24

file_path ='C:/Users/d-het/PycharmProjects/moddet1/temperatures.csv'
temperature_data = load_temperature_data(file_path)

def update_temperature2(u, room, t, alpha, dt, P, rho, c, S, temperature_data):
    u_new = np.copy(u)
    z=0
    for i in range(1, room.n1 - 1):
        for j in range(1, room.k1 - 1):
            if (i, j) in room.wall_positions:
                continue

            laplacian = (u[i + 1, j] + u[i - 1, j] + u[i, j + 1] + u[i, j - 1] - 4 * u[i, j]) / (room.hx ** 2)
            u_new[i, j] = u[i, j] + alpha * laplacian * dt

            if (i, j) in room.radiator_positions:
                avg_temp = np.mean(u[room.grid == 1])
                if avg_temp < S:
                    if len(room.radiator_positions) > 5:
                        c1 = len(room.radiator_positions) / 2
                        u_new[i, j] += (P / (rho * c * c1))
                        z += (P / (rho * c * c1))
                    else:
                        u_new[i, j] += (P / (rho * c * len(room.radiator_positions)))
                        z += (P / (rho * c * len(room.radiator_positions)))

    for (i, j) in room.wall_positions:
        if i == 0:
            u_new[i, j] = u[i + 1, j]
        elif i == room.n1 - 1:
            u_new[i, j] = u[i - 1, j]
        elif j == 0:
            u_new[i, j] = u[i, j + 1]
        elif j == room.k1 - 1:
            u_new[i, j] = u[i, j - 1]

    for (i, j) in room.window_positions:
        t_index = int(t / dt) % len(temperature_data)
        u_new[i, j] = temperature_data[t_index]

    return u_new, z


u1 = np.zeros((house.n1, house.k1 + kitchen.k1))
u1[:, :] = 293

u = np.zeros((house.n1, house.k1))
u[:, :] = 293

u2 = np.zeros((kitchen.n1, kitchen.k1))
u2[:, :] = 293

u3 = np.zeros((bathroom.n1, bathroom.k1))
u3[:, :] = 293

upper_door_means = []
lower_door_means = []
combined_heat = []
z_values1 = []
time_steps = []
z_total=0
for t in np.arange(0, total_time, dt):
    u, z1 = update_temperature2(u, house, t, alpha, dt, P, rho, c, S,temperature_data)
    u2, z2 = update_temperature2(u2, kitchen, t, alpha, dt, P, rho, c, S, temperature_data)
    u3, z3 = update_temperature2(u3, bathroom, t, alpha, dt, P, rho, c, S, temperature_data)

    z_total += z1 + z2 + z3
    z_values1.append(z_total)
    time_steps.append(t)

    u1[:, :house.k1] = u
    u1[bathroom.n1:, kitchen.k1:] = u2
    u1[:bathroom.n1, kitchen.k1:] = u3

    upper_door_positions = [
            (i, j) for (i, j) in house.door_positions if i < house.n1 / 2
        ] + [
            (i, j + house.k1) for (i, j) in kitchen.door_positions if i < kitchen.n1 / 2
        ]

    lower_door_positions = [
            (i, j) for (i, j) in house.door_positions if i >= house.n1 / 2
        ] + [
            (i, j + house.k1) for (i, j) in bathroom.door_positions if i >= bathroom.n1 / 2
        ]

    upper_door_mean, lower_door_mean = calculate_door_means(u1, upper_door_positions, lower_door_positions)
    upper_door_means.append(upper_door_mean)
    lower_door_means.append(lower_door_mean)

    update_door_temperatures(u1, upper_door_positions)
    update_door_temperatures(u1, lower_door_positions)

    combined_heat.append(u1.copy())

    u = u1[:, :house.k1]
    u2 = u1[bathroom.n1:, kitchen.k1:]
    u3 = u1[:bathroom.n1, kitchen.k1:]




plt.figure(figsize=(10, 6))
plt.imshow(combined_heat[960], cmap='hot', interpolation='nearest', origin='lower')
plt.colorbar(label='Temperature (K)')
plt.xlabel('X Position')
plt.ylabel('Y Position')
plt.show()


animate_heat_distribution(combined_heat)

plt.figure(figsize=(10, 6))
plt.plot(time_steps, z_values, label='Heat Added by Radiators with turned off radiators')
plt.plot(time_steps, z_values1, label='Heat Added by Radiators')
plt.xlabel('Time (hours)')
plt.ylabel('Heat Added (z)')
plt.title('Heat Added by Radiators Over Time')
plt.legend()
plt.grid()
plt.show()
