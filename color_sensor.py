import bpy
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

from utils import rotate_vector


class Floor:
    def __init__(self, floor_matrix, *, px_unit_mm=5, center_point=(0, 0)):
        self.matrix = floor_matrix
        self.px_unit = px_unit_mm

        self.offset_px = np.subtract(np.divide(self.matrix.shape[0:2], 2), center_point)
        self.center_point_offset = np.multiply(self.offset_px, self.px_unit)

    def get_value_at_position(self, x, y):
        index = (x / self.px_unit, y / self.px_unit)
        index = np.add(index, np.divide(self.matrix.shape[0:2], 2))
        index = np.subtract(index, self.offset_px)
        index = (int(index[0]), int(index[1]))
        return self.matrix[index]

    def get_scale(self):
        s = self.matrix.shape[0] / (5 / self.px_unit)
        return [s, s, 1]

    def get_location(self, z=0):
        return np.append(self.center_point_offset, z)


class ColorSensor:
    def __init__(self, position_offsets, floor):
        self.position_offsets = position_offsets
        self.floor = floor

    def read(self, car_position, car_rotation_z):
        car = (car_position[0], car_position[1])

        p0 = np.add(car, rotate_vector(self.position_offsets[0], [0, 0, car_rotation_z])[0:2])
        p1 = np.add(car, rotate_vector(self.position_offsets[1], [0, 0, car_rotation_z])[0:2])
        p2 = np.add(car, rotate_vector(self.position_offsets[2], [0, 0, car_rotation_z])[0:2])
        p3 = np.add(car, rotate_vector(self.position_offsets[3], [0, 0, car_rotation_z])[0:2])
        p4 = np.add(car, rotate_vector(self.position_offsets[4], [0, 0, car_rotation_z])[0:2])

        return [
            self.floor.get_value_at_position(x=p0[0], y=p0[1]),
            self.floor.get_value_at_position(x=p1[0], y=p1[1]),
            self.floor.get_value_at_position(x=p2[0], y=p2[1]),
            self.floor.get_value_at_position(x=p3[0], y=p3[1]),
            self.floor.get_value_at_position(x=p4[0], y=p4[1])
        ]


if __name__ == '__main__':
    floor_matrix = np.asarray(Image.open('path.png').convert('L'))
    floor = Floor(floor_matrix)

    print(floor.get_value_at_position(x=0, y=0))

    plt.imshow(floor_matrix, cmap='gray')
    plt.show()
