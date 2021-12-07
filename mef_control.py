from enum import Enum
import utils

class State(Enum):
    START = 1

    STRAIGHT = 3
    TURN_LEFT_LOW = 31
    TURN_LEFT_HIGH = 32
    TURN_RIGHT_LOW = 33
    TURN_RIGHT_HIGH = 34

    SLOWDOWN = 5
    STOP = 51
    BACKWARD = 52
    MOVE_AROUND_OBJECT = 53

    END = 7


class MefControl:
    MAX_SPEED = 200
    MAX_ACCELERATION = 500

    SLOWDOWN_SPEED = 150
    BACKWARD_SPEED = -166
    MOVE_AROUND_OBJECT_SPEED = 166

    SLOWDOWN_DISTANCE = 40

    THRESHOLD_COLOR_SENSOR = 80

    TURNING_ANGLE_HEAVY = 60
    TURNING_ANGLE_LOW = 5

    def __init__(self, car):
        self.car = car
        self.state = State.START
        self.next_state = State.START
        self.frames_MOVE_AROUND_OBJECT = 0

    def update(self):
        self.setNextState()
        self.setState()
        self.setOutput()

    def setState(self):
        self.state = self.next_state

    def set_follow_line_next_state(self, line):
        if line == "middle":
            self.next_state = State.STRAIGHT
            return True
        elif line == "left":
            self.next_state = State.TURN_LEFT_LOW
            return True
        elif line == "big_left":
            self.next_state = State.TURN_LEFT_HIGH
            return True
        elif line == "right":
            self.next_state = State.TURN_RIGHT_LOW
            return True
        elif line == "big_right":
            self.next_state = State.TURN_RIGHT_HIGH
            return True
        return False

    def set_final_line_next_state(self, line):
        if line == "all":
            self.next_state = State.END
            return True
        return False

    def setNextState(self):
        print(f"state : {self.state}")
        if self.state == State.START:
            self.next_state = State.STRAIGHT
        elif self.state == State.STRAIGHT or self.state == State.TURN_LEFT_LOW or self.state == State.TURN_RIGHT_LOW or self.state == State.SLOWDOWN:
            line = self.get_line()
            if self.set_final_line_next_state(line): return

            dist = self.car.distance_sensor.read(self.car.get_location(), self.car.get_rotation()[2])
            if 0 <= dist <= 10:
                self.next_state = State.STOP
                return
            elif 0 <= dist <= MefControl.SLOWDOWN_DISTANCE:
                self.next_state = State.SLOWDOWN
                return

            self.set_follow_line_next_state(line)
            return

        elif self.state == State.TURN_LEFT_HIGH or self.state == State.TURN_RIGHT_HIGH:
            line = self.get_line()
            if self.set_final_line_next_state(line): return

            self.set_follow_line_next_state(line)
            return
        elif self.state == State.STOP:
            self.next_state = State.BACKWARD

        elif self.state == State.BACKWARD:
            distance_sensor_value = self.car.distance_sensor.read(self.car.get_location(), self.car.get_rotation()[2])
            if distance_sensor_value < 30:
                self.next_state = State.BACKWARD
            else:
                self.next_state = State.MOVE_AROUND_OBJECT
        elif self.state == State.MOVE_AROUND_OBJECT:
            line = self.get_line()
            if self.frames_MOVE_AROUND_OBJECT > 500 and line == "big_left":
                self.next_state = State.TURN_LEFT_HIGH
                self.frames_MOVE_AROUND_OBJECT = 0 # reset for next object
            else:
                self.next_state = State.MOVE_AROUND_OBJECT
        elif self.state == State.END:
            self.next_state = State.END

    def setOutput(self):
        if self.state == State.STRAIGHT or self.state == State.TURN_LEFT_LOW or self.state == State.TURN_RIGHT_LOW or self.state == State.TURN_LEFT_HIGH or self.state == State.TURN_RIGHT_HIGH:
            if self.car.get_speed() < MefControl.MAX_SPEED:
                self.car.acceleration = utils.rotate_vector([0, 0, -MefControl.MAX_ACCELERATION], self.car.get_rotation())
            else :
                self.car.acceleration = [0, 0, 0]
        if self.state == State.START:
            self.car.acceleration = [0, 0, 0]
        elif self.state == State.STRAIGHT:
            self.car.set_front_wheel_angle(0)
        elif self.state == State.TURN_LEFT_LOW:
            self.car.set_front_wheel_angle(MefControl.TURNING_ANGLE_LOW)
        elif self.state == State.TURN_LEFT_HIGH:
            self.car.set_front_wheel_angle(MefControl.TURNING_ANGLE_HEAVY)
        elif self.state == State.TURN_RIGHT_LOW:
            self.car.set_front_wheel_angle(-MefControl.TURNING_ANGLE_LOW)
        elif self.state == State.TURN_RIGHT_HIGH:
            self.car.set_front_wheel_angle(-MefControl.TURNING_ANGLE_HEAVY)
        elif self.state == State.SLOWDOWN:
            if self.car.get_speed() < MefControl.SLOWDOWN_SPEED:
                self.car.acceleration = utils.rotate_vector([0, 0, -MefControl.MAX_ACCELERATION], self.car.get_rotation())
            else :
                self.car.acceleration = [0, 0, 0]
        elif self.state == State.STOP:
            self.car.velocity = [0, 0, 0]
        elif self.state == State.BACKWARD:
            #PAUSE
            if self.frames_MOVE_AROUND_OBJECT < 300:
                self.car.acceleration = [0, 0, 0]
                self.car.set_speed(0)
                self.frames_MOVE_AROUND_OBJECT += 1
            # RECULON
            else:
                self.car.set_front_wheel_angle(0)
                if self.car.get_speed() < -MefControl.BACKWARD_SPEED:
                    self.car.acceleration = utils.rotate_vector([0, 0, MefControl.MAX_ACCELERATION], self.car.get_rotation())
                else:
                    self.car.acceleration = [0, 0, 0]
        elif self.state == State.MOVE_AROUND_OBJECT:
            if self.frames_MOVE_AROUND_OBJECT == 300:
                self.car.set_speed(0)
            # CONTOURNER
            if self.frames_MOVE_AROUND_OBJECT < 400:
                self.car.set_front_wheel_angle(40)
                if self.car.get_speed() < MefControl.MOVE_AROUND_OBJECT_SPEED:
                    self.car.acceleration = utils.rotate_vector([0, 0, -MefControl.MAX_ACCELERATION], self.car.get_rotation())
                else:
                    self.car.acceleration = [0, 0, 0]
            else:
                self.car.acceleration = [0, 0, 0]
                self.car.set_front_wheel_angle(-40)
            self.frames_MOVE_AROUND_OBJECT += 1
        elif self.state == State.END:
            self.car.acceleration = [0, 0, 0]
            self.car.set_speed(0)

    def get_line(self):
        colors = self.car.color_sensor.read(self.car.get_location(), self.car.get_rotation()[2])

        print(colors)

        nb = sum([c < MefControl.THRESHOLD_COLOR_SENSOR for c in colors])

        if nb == 0:
            return "none"
        if nb == 5:
            return "all"

        if colors[2] < MefControl.THRESHOLD_COLOR_SENSOR:
            return "middle"
        elif colors[1] < MefControl.THRESHOLD_COLOR_SENSOR:
            return "left"
        elif colors[3] < MefControl.THRESHOLD_COLOR_SENSOR:
            return "right"
        elif colors[0] < MefControl.THRESHOLD_COLOR_SENSOR:
            return "big_left"
        elif colors[4] < MefControl.THRESHOLD_COLOR_SENSOR:
            return "big_right"
        else:
            return "wtf"
