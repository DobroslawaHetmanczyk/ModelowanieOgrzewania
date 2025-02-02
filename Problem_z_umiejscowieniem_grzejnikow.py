import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from plan_mieszkania import salon, Kuchnia, Lazienka

def T_out(t):
    return 273 + 5 * np.sin(t / 10)

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
ht = 0.0001
dt = 0.01
S = 298
P = 2000
rho = 1.225
c = 1005
total_time = 66

def update_temperature(u, room, t, alpha, dt, P, rho, c, S):
    u_new = np.copy(u)
    for i in range(1, room.n1 - 1):
        for j in range(1, room.k1 - 1):
            if (i, j) in room.wall_positions:
                continue

            laplacian = (u[i + 1, j] + u[i - 1, j] + u[i, j + 1] + u[i, j - 1] - 4 * u[i, j]) / (room.hx ** 2)
            u_new[i, j] = u[i, j] + alpha * laplacian * dt

            if (i, j) in room.radiator_positions:
                avg_temp = np.mean(u[room.grid == 1])
                if avg_temp <= S:
                    u_new[i, j] += (P / (rho * c * len(room.radiator_positions)))

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
        u_new[i, j] = T_out(t)

    return u_new

def calculate_door_means(u1, upper_door_positions, lower_door_positions):
    upper_door_mean = np.nanmean([u1[i, j] for (i, j) in upper_door_positions])
    lower_door_mean = np.nanmean([u1[i, j] for (i, j) in lower_door_positions])
    return upper_door_mean, lower_door_mean

def update_door_temperatures(u1, door_positions):
    for (i, j) in door_positions:
        neighbors = [u1[i, j]]

        if i > 0 and not np.isnan(u1[i - 1, j]):
            neighbors.append(u1[i - 1, j])
        if i < u1.shape[0] - 1 and not np.isnan(u1[i + 1, j]):
            neighbors.append(u1[i + 1, j])
        if j > 0 and not np.isnan(u1[i, j - 1]):
            neighbors.append(u1[i, j - 1])
        if j < u1.shape[1] - 1 and not np.isnan(u1[i, j + 1]):
            neighbors.append(u1[i, j + 1])

        u1[i, j] = np.mean(neighbors)

def simulate(house, kitchen, bathroom, total_time, dt):
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
    for t in np.arange(0, total_time, dt):
        u = update_temperature(u, house, t, alpha, dt, P, rho, c, S)
        u2 = update_temperature(u2, kitchen, t, alpha, dt, P, rho, c, S)
        u3 = update_temperature(u3, bathroom, t, alpha, dt, P, rho, c, S)

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

    return combined_heat


combined_heat = simulate(house, kitchen, bathroom, total_time, dt)


fig, ax = plt.subplots(figsize=(10, 6))
im = ax.imshow(combined_heat[0], cmap='hot', interpolation='nearest', origin='lower', animated=True, vmin=270, vmax=310)
plt.colorbar(im, label='Temperature (K)')
plt.xlabel('X Position')
plt.ylabel('Y Position')

def update(frame):
    im.set_array(combined_heat[frame])
    ax.set_title(f'Time Step: {frame * dt:.2f} hours')
    return im,

ani = animation.FuncAnimation(fig, update, frames=len(combined_heat), interval=50, blit=False)
plt.show()

plt.figure(figsize=(10, 6))
plt.imshow(combined_heat[-1], cmap='hot', interpolation='nearest', origin='lower', vmin=270, vmax=310)
plt.colorbar(label='Temperature (K)')
plt.xlabel('X Position')
plt.ylabel('Y Position')
plt.title(f'Final Temperature Distribution at Time Step: {total_time:.2f} hours')
plt.show()