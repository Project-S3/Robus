from enum import Enum
import utils
import numpy as np

class State(Enum):
    START = 1
    ACCELERATION = 2
    TURN = 3
    MAX_SPEED = 4
    STOP = 5
    GET_AROUND_OBJECT = 6
    END = 7


class MefControl:
    def __init__(self, car):
        self.car = car
        self.state = State.START
        self.next_state = State.START
        self.angle_rotation_wheels = 0

        self.MAX_SPEED = 200
        self.MAX_ACCELERATION = 500

        self.THRESHOLD_COLOR_SENSOR = 30
        self.ANGLE_SMALL_ROTATION = 2
        self.ANGLE_BIG_ROTATION = 25

    def update(self):
        self.setNextState()
        self.setState()
        self.setOutput()

    def setState(self):
        self.state = self.next_state

    def setNextState(self):
        print(f"state : {self.state}")
        print(f"self.car.wheel_angle : {self.car.wheel_angle}")
        if self.check_color_sensor() == 2:
            self.next_state = State.END
            return
        if self.state == State.START:
            self.next_state = State.ACCELERATION
        elif self.state == State.ACCELERATION:
            if self.check_distance_sensor() == 1:
                self.next_state = State.STOP
            elif self.car.get_speed() >= self.MAX_SPEED:
                self.next_state = State.MAX_SPEED
            elif self.check_color_sensor() == 1:
                self.next_state = State.TURN
            else:
                self.next_state = State.ACCELERATION
        elif self.state == State.TURN:
            if self.check_color_sensor() == 1:
                self.next_state = State.TURN
            elif self.car.get_speed() >= self.MAX_SPEED:
                self.next_state = State.MAX_SPEED
            else:
                self.next_state = State.ACCELERATION
        elif self.state == State.MAX_SPEED:
            if self.check_distance_sensor() == 1:
                self.next_state = State.STOP
            elif self.check_color_sensor() == 1:
                self.next_state = State.TURN
            else:
                self.next_state = State.MAX_SPEED
        elif self.state == State.STOP:
            print(f"speed : {self.car.get_speed()}")
            if self.car.get_speed() <= 10:
                self.next_state = State.GET_AROUND_OBJECT
            else:
                self.next_state = State.STOP
        elif self.state == State.GET_AROUND_OBJECT:
            if self.check_color_sensor() == -1:
                self.next_state = State.GET_AROUND_OBJECT
            else:
                #self.next_state = State.ACCELERATION
                self.next_state = State.END
        elif self.state == State.END:
            self.next_state = State.END

    def setOutput(self):
        if self.state == State.START:
            self.car.acceleration = [0, 0, 0]
        elif self.state == State.ACCELERATION:
            self.car.acceleration = utils.rotate_vector([0, 0, -self.MAX_ACCELERATION], self.car.get_rotation())
        elif self.state == State.TURN:
            color_sensor_values = self.car.color_sensor.read(self.car.get_location(), self.car.get_rotation()[2])
            if color_sensor_values[0] < self.THRESHOLD_COLOR_SENSOR or color_sensor_values[1] < self.THRESHOLD_COLOR_SENSOR:
                if color_sensor_values[0] < self.THRESHOLD_COLOR_SENSOR:
                    self.angle_rotation_wheels = self.ANGLE_BIG_ROTATION
                else:
                    self.angle_rotation_wheels = self.ANGLE_SMALL_ROTATION
            elif color_sensor_values[3] < self.THRESHOLD_COLOR_SENSOR or color_sensor_values[4] < self.THRESHOLD_COLOR_SENSOR:
                if color_sensor_values[4] < self.THRESHOLD_COLOR_SENSOR:
                    self.angle_rotation_wheels = -self.ANGLE_BIG_ROTATION
                else:
                    self.angle_rotation_wheels = -self.ANGLE_SMALL_ROTATION
            self.car.set_front_wheel_angle(self.angle_rotation_wheels)
        elif self.state == State.MAX_SPEED:
            self.car.acceleration = [0, 0, 0]
        elif self.state == State.STOP:
            self.car.acceleration = utils.rotate_vector([0, 0, self.MAX_ACCELERATION], self.car.get_rotation())
        elif self.state == State.GET_AROUND_OBJECT:
            self.car.acceleration = [0, 0, 0]
            self.car.set_speed(0)
            # TODO
        elif self.state == State.END:
            self.car.acceleration = [0, 0, 0]
            self.car.set_speed(0)

    def check_color_sensor(self):
        # 0 = sur la ligne
        # -1 = pas de ligne détectée
        # 1 = trop à droite ou à gauche
        # 2 = fin détectée (T)
        color_sensor_values = self.car.color_sensor.read(self.car.get_location(), self.car.get_rotation()[2])
        print(f"color_sensor_values : {color_sensor_values}")
        nb = 0
        for val in color_sensor_values:
            if val < self.THRESHOLD_COLOR_SENSOR:
                nb = nb + 1
        if nb == 5:
            return 2
        elif nb == 0:
            return -1
        elif color_sensor_values[2] < self.THRESHOLD_COLOR_SENSOR:
            return 0
        else:
            return 1

    def check_distance_sensor(self):
        # 0 = pas d'objet
        # 1 = objet détecté

        distance_sensor_value = self.car.distance_sensor.read(self.car.get_location(), self.car.get_rotation()[2])
        if 0 <= distance_sensor_value <= 30:
            return 1
        else:
            return 0
