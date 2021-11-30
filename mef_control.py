from enum import Enum
import utils


class State(Enum):
    START = 1
    ACCELERATION = 2
    TURN_LEFT = 3
    TURN_RIGHT = 4
    MAX_SPEED = 5
    STOP = 6
    GET_AROUND_OBJECT = 7
    STOP_FOR_END = 8
    END = 9


class MefControl:
    def __init__(self, car):
        self.car = car
        self.state = State.START
        self.next_state = State.START

        self.MAX_SPEED = 20
        self.MAX_ACCELERATION = 5

    def update(self):
        self.setNextState()
        self.setState()
        print(self.state)
        self.setOutput()

    def setState(self):
        self.state = self.next_state

    def setNextState(self):
        if self.check_color_sensor() == 3:
            self.next_state = State.STOP_FOR_END
            return
        if self.state == State.START:
            self.next_state = State.ACCELERATION
        elif self.state == State.ACCELERATION:
            if self.check_distance_sensor() == 1:
                self.next_state = State.STOP
            elif self.car.get_speed() >= self.MAX_SPEED:
                self.next_state = State.MAX_SPEED
            elif self.check_color_sensor() == 1:
                self.next_state = State.TURN_LEFT
            elif self.check_color_sensor() == 2:
                self.next_state = State.TURN_RIGHT
            else:
                self.next_state = State.ACCELERATION
        elif self.state == State.TURN_LEFT:
            if self.car.get_speed() >= self.MAX_SPEED:
                self.next_state = State.MAX_SPEED
            else:
                self.next_state = State.ACCELERATION
        elif self.state == State.TURN_RIGHT:
            if self.car.get_speed() >= self.MAX_SPEED:
                self.next_state = State.MAX_SPEED
            else:
                self.next_state = State.ACCELERATION
        elif self.state == State.MAX_SPEED:
            if self.check_distance_sensor() == 1:
                self.next_state = State.STOP
            elif self.check_color_sensor() == -1:
                self.next_state = State.TURN_LEFT
            elif self.check_color_sensor() == 1:
                self.next_state = State.TURN_RIGHT
            else:
                self.next_state = State.MAX_SPEED
        elif self.state == State.STOP:
            if self.car.get_speed() == 0:
                self.next_state = State.GET_AROUND_OBJECT
            else:
                self.next_state = State.STOP
        elif self.state == State.GET_AROUND_OBJECT:
            if self.check_color_sensor() == -1:
                self.next_state = State.GET_AROUND_OBJECT
            else:
                self.next_state = State.ACCELERATION
        elif self.state == State.STOP_FOR_END:
            if self.car.get_speed() == 0:
                self.next_state = State.END
            else:
                self.next_state = State.STOP_FOR_END
        elif self.state == State.END:
            self.next_state = State.END

    def setOutput(self):
        if self.state == State.START:
            self.car.acceleration = [0, 0, 0]
            self.car.set_front_wheel_angle(0)
        elif self.state == State.ACCELERATION:
            self.car.acceleration = utils.rotate_vector([self.MAX_ACCELERATION, 0, 0], self.car.get_rotation())
        elif self.state == State.TURN_LEFT:
            self.car.set_front_wheel_angle(5)
        elif self.state == State.TURN_RIGHT:
            self.car.set_front_wheel_angle(-5)
        elif self.state == State.MAX_SPEED:
            self.car.acceleration = [0, 0, 0]
        elif self.state == State.STOP:
            #self.car.acceleration = utils.rotate_vector([-self.MAX_ACCELERATION, 0, 0], self.car.get_rotation())
            self.car.set_speed(0)
        elif self.state == State.GET_AROUND_OBJECT:
            pass
            # TODO
        elif self.state == State.STOP_FOR_END:
            self.car.acceleration = utils.rotate_vector([-self.MAX_ACCELERATION, 0, 0], self.car.get_rotation())
        elif self.state == State.END:
            self.car.acceleration = [0, 0, 0]
            self.car.velocity = [0, 0, 0]

    def check_color_sensor(self):
        # 0 = sur la ligne
        # -1 = pas de ligne détectée
        # 1 = trop à droite
        # 2 = trop à gauche
        # 3 = fin détectée (T)
        return 0

    def check_distance_sensor(self):
        # 0 = pas d'objet
        # 1 = objet détecté

        distanceSensorValue = self.car.distance_sensor.read(self.car.get_location(), self.car.get_rotation()[2])
        if 0 <= distanceSensorValue <= 10:
            return 1
        else:
            return 0
