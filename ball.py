from framer import *


def obj_update(ball, time, entities, changes):
    ball.rotate_velocity(changes["delta_rotation"])
    ball.set_acceleration_from_car()
    ball.set_location_y()


class Ball(Entity):
    def __init__(self, blender_object_name, car):
        super().__init__(blender_object_name)
        self.update_callback = obj_update
        self.car = car
        children = {ob.name: ob for ob in self.car.blender_object.children}
        self.plate = children["Plate"]

    def set_acceleration_from_car(self):
        angle = self.get_distance_from_center() / np.sqrt(
            np.power(140, 2) - np.power(self.get_distance_from_center(), 2))
        acc_ball_center = 9.81 * np.cos(angle) * np.sin(angle) * 1000

        ball_velocity = np.subtract(self.velocity, self.car.velocity)

        if ball_velocity[0] > 0:
            signe_friction_x = -1
        elif ball_velocity[0] < 0:
            signe_friction_x = 1
        else:
            signe_friction_x = 0

        if ball_velocity[1] > 0:
            signe_friction_y = -1
        elif ball_velocity[1] < 0:
            signe_friction_y = 1
        else:
            signe_friction_y = 0

        friction = 9.81 * 0.006 * np.power(np.cos(angle), 2) * 1000

        self.acceleration[0] = acc_ball_center * np.cos(self.get_direction_acc_ball_center()) + self.car.acceleration[
            0] + signe_friction_x * friction
        self.acceleration[1] = acc_ball_center * np.sin(self.get_direction_acc_ball_center()) + self.car.acceleration[
            1] + signe_friction_y * friction

    def set_location_y(self):
        self.blender_object.location[2] = 140 - np.sqrt(
            np.power(140, 2) - np.power(self.get_distance_from_center(), 2)) + 43.75

    def get_plate_location(self):
        plate_location = [0, 39, 39]
        return np.add(self.car.get_location(), self.rotate_vector(plate_location, [0, 0, self.car.get_rotation()[2]]))

    def get_distance_from_center(self):
        print(self.get_plate_location())
        x = self.get_location()[0] - self.get_plate_location()[0]
        y = self.get_location()[1] - self.get_plate_location()[1]
        print(np.sqrt(np.power(x, 2) + np.power(y, 2)))
        return np.sqrt(np.power(x, 2) + np.power(y, 2))

    def get_direction_acc_ball_center(self):
        x = self.get_plate_location()[0] - self.get_location()[0]
        y = self.get_plate_location()[1] - self.get_location()[1]
        if y == 0:
            direction = 0
        elif x == 0:
            direction = np.pi / 2
        else:
            direction = np.arctan(y / x)
        if x < 0:
            direction += np.pi
        return direction

    def rotate_vector(self, vec, rotation):
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
