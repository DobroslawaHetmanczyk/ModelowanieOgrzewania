import numpy as np
import matplotlib.pyplot as plt

class salon:
    def __init__(self, od1, do1, od2, do2, hx):
        self.y_min = od1
        self.y_max = do1
        self.x_min = od2
        self.x_max = do2
        self.hx = hx
        y1 = np.linspace(od1, do1, int((abs(do1 - od1)) / hx) + 1)
        x1 = np.linspace(od2, do2, int((abs(do2 - od2)) / hx) + 1)
        self.n1 = len(y1)
        self.k1 = len(x1)
        self.x1, self.y1 = np.meshgrid(x1, y1)
        self.grid = np.full((self.n1, self.k1), 1)

        self.window_positions = []
        self.door_positions = []
        self.wall_positions = []
        self.radiator_positions = []

    def add_wall(self):
        self.grid[:, 0] = 0
        self.grid[:, self.k1 - 1] = 0
        self.grid[0, :] = 0
        self.grid[self.n1 - 1, :] = 0

        self.wall_positions = [(i, j) for i in range(self.n1) for j in range(self.k1) if self.grid[i, j] == 0]

    def add_door(self):
        mid_col = self.k1 - 1
        for i in range(int(self.n1 * 1 / 10), int(self.n1 * 2 / 10)):
            self.grid[i, mid_col] = 4

        for i in range(int(self.n1 * 7 / 10), int(self.n1 * 8 / 10)):
            self.grid[i, mid_col] = 4

        self.door_positions = [(i, mid_col) for i in range(int(self.n1 * 1 / 10), int(self.n1 * 2 / 10))] + \
                              [(i, mid_col) for i in range(int(self.n1 * 7 / 10), int(self.n1 * 8 / 10))]

    def add_window(self):
        for i in range(int(self.n1 / 5), int(self.n1 * 2 / 5)):
            self.grid[i, 0] = 2

        for i in range(int(self.n1 * 3 / 5), int(self.n1 * 4 / 5)):
            self.grid[i, 0] = 2

        self.window_positions = [(i, 0) for i in range(int(self.n1 / 5), int(self.n1 * 2 / 5))] + \
                                [(i, 0) for i in range(int(self.n1 * 3 / 5), int(self.n1 * 4 / 5))]

    def add_radiator(self):
        mid_col = self.k1 - 1
        for i in range(int(self.n1 * 2 / 5), int(self.n1 * 3 / 5)):
            self.grid[i, mid_col - 1] = 3

        self.radiator_positions = [(i, mid_col - 1) for i in range(int(self.n1 * 2 / 5), int(self.n1 * 3 / 5))]




class Kuchnia:
    def __init__(self, od1, do1, od2, do2, hx):
        self.y_min = od1
        self.y_max = do1
        self.x_min = od2
        self.x_max = do2
        self.hx = hx
        y1 = np.linspace(od1, do1, int((abs(do1 - od1)) / hx) + 1)
        x1 = np.linspace(od2, do2, int((abs(do2 - od2)) / hx) + 1)
        self.n1 = len(y1)
        self.k1 = len(x1)
        self.x1, self.y1 = np.meshgrid(x1, y1)
        self.grid = np.full((self.n1, self.k1), 1)

        self.door_positions = []
        self.window_positions = []
        self.radiator_positions = []
        self.wall_positions = []
    def add_wall(self):
        self.grid[:, 0] = 0
        self.grid[:, self.k1 - 1] = 0
        self.grid[0, :] = 0
        self.grid[self.n1 - 1, :] = 0

        self.wall_positions = [(i, 0) for i in range(self.n1)] + \
                              [(i, self.k1 - 1) for i in range(self.n1)] + \
                              [(0, j) for j in range(self.k1)] + \
                              [(self.n1 - 1, j) for j in range(self.k1)]

    def add_door(self):
        for i in range(int(self.n1 * 1 / 4), int(self.n1 * 1 / 2)):
            self.grid[i, 0] = 4
            self.door_positions.append((i, 0))

    def add_window(self):
        mid_col = self.k1 - 1
        for i in range(int(self.n1 / 4), int(self.n1 * 3 / 4)):
            self.grid[i, mid_col] = 2
            self.window_positions.append((i, mid_col))

    def add_radiator(self):
        for i in range(int(self.k1 * 1 / 4), int(self.k1 * 3 / 4)):
            self.grid[self.n1-2, i] = 3
            self.radiator_positions.append((self.n1-2, i))


class Lazienka:
    def __init__(self, od1, do1, od2, do2, hx):
        self.y_min = od1
        self.y_max = do1
        self.x_min = od2
        self.x_max = do2
        self.hx = hx
        y1 = np.linspace(od1, do1, int((abs(do1 - od1)) / hx) + 1)
        x1 = np.linspace(od2, do2, int((abs(do2 - od2)) / hx) + 1)
        self.n1 = len(y1)
        self.k1 = len(x1)
        self.x1, self.y1 = np.meshgrid(x1, y1)
        self.grid = np.full((self.n1, self.k1), 1)

        self.door_positions = []
        self.window_positions = []
        self.radiator_positions = []
        self.wall_positions = []

    def add_wall(self):
        self.grid[:, 0] = 0
        self.grid[:, self.k1 - 1] = 0
        self.grid[0, :] = 0
        self.grid[self.n1 - 1, :] = 0

        self.wall_positions = [(i, 0) for i in range(self.n1)] + \
                              [(i, self.k1 - 1) for i in range(self.n1)] + \
                              [(0, j) for j in range(self.k1)] + \
                              [(self.n1 - 1, j) for j in range(self.k1)]

    def add_door(self):
        for i in range(int(self.n1 * 5 / 30), int(self.n1 / 3)):
            self.grid[i, 0] = 4
            self.door_positions.append((i, 0))

    def add_window(self):
        for i in range(int(self.n1 / 3), int(self.n1 * 2 / 3)):
            self.grid[i, self.k1 - 1] = 2
            self.window_positions.append((i, self.k1 - 1))

    def add_radiator(self):
        for i in range(int(self.n1 / 3), int(self.n1 * 2 / 3)):
            self.grid[i, self.k1 - 2] = 3
            self.radiator_positions.append((i, self.k1 - 2))



hx = 0.1
house = salon(-1, 1, -1, 0, hx)
kitchen = Kuchnia(0.2,1,0,1, hx)
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

big_matrix = np.full((house.n1, house.k1 * 2 ), np.nan)
big_matrix[:, :house.k1] = house.grid
big_matrix[bathroom.n1 :, kitchen.k1:] = kitchen.grid
big_matrix[:bathroom.n1 , kitchen.k1:] = bathroom.grid

plt.imshow(big_matrix, cmap="viridis", origin="lower")
plt.colorbar(label="Grid values")
plt.title("House Layout")
plt.show()