import numpy as np

import framer


def obj_update(car, time, entities, changes):
    car.velocity = rotate_vector(car.velocity, changes["delta_rotation"])
    car.acceleration = rotate_vector(car.acceleration, changes["delta_rotation"])
    if time > 10:
        print("lol")
        car.angular_velocity = [0, 0, -np.pi/6]


class Car(framer.Entity):
    def __init__(self, blender_object_name):
        super().__init__(blender_object_name)
        self.update_callback = obj_update

    def get_speed(self):
        return np.linalg.norm(self.velocity)

    def set_speed(self, speed):
        if self.get_speed() == 0:
            self.velocity = [speed, 0, 0]
        else:
            self.velocity = set_module_vector(self.velocity, speed)

    def set_front_wheel_angle(self):
        pass


def rotate_vector(vec, rotation):
    v = np.array(vec)
    rx = np.array([[1, 0, 0],
                   [0, np.cos(rotation[0]), -np.sin(rotation[0])],
                   [0, np.sin(rotation[0]), np.cos(rotation[0])]])
    ry = np.array([[np.cos(rotation[1]), 0, np.sin(rotation[1])],
                   [0, 1, 0],
                   [-np.sin(rotation[1]), 0, np.cos(rotation[1])]])
    rz = np.array([[np.cos(rotation[2]), -np.sin(rotation[2]), 0],
                   [np.sin(rotation[2]), np.cos(rotation[2]), 0],
                   [0, 0, 1]])
    v = rx @ v
    v = ry @ v
    v = rz @ v
    return v.tolist()


def set_module_vector(vec, new_module):
    if new_module == 0: return [0, 0, 0]
    factor = np.linalg.norm(vec) / new_module
    return np.divide(vec, factor)
