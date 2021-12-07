import time
from enum import Enum

from car import Car
from wheels import Wheels

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
    INIT_SPEED = 50 # 60
    MAX_SPEED = 60 # 80

    SLOWDOWN_SPEED = 45
    BACKWARD_SPEED = -50
    MOVE_AROUND_OBJECT_SPEED = 50

    SLOWDOWN_DISTANCE = 40

    THRESHOLD_COLOR_SENSOR = 50

    def __init__(self, car: Car):
        self.car = car
        self.state = State.START
        self.previous_state = None
        self.next_state = State.START
        self.frames_get_around_object = 0

        
    def update(self):
        self.setNextState()
        self.setOutput()
        self.setState()
        return self.previous_state == State.END

    def setState(self):
        self.previous_state = self.state
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
        if self.previous_state != self.state: print(f"Current State : {self.state}")

        if self.state == State.START:
            self.next_state = State.STRAIGHT
            return

        elif self.state == State.STRAIGHT or self.state == State.TURN_LEFT_LOW or self.state == State.TURN_RIGHT_LOW or self.state == State.SLOWDOWN:
            line = self.get_line()
            if self.set_final_line_next_state(line): return

            dist = self.car.read_distance()
            if 0 <= dist <= 10 + 2:
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
            return

        elif self.state == State.BACKWARD:
            if self.previous_state != State.BACKWARD:
                time.sleep(5)
            elif self.car.read_distance() >= 25: self.next_state = State.MOVE_AROUND_OBJECT
            return

        elif self.state == State.MOVE_AROUND_OBJECT:
            line = self.get_line()
            if line == "big_left":
                self.next_state = State.TURN_LEFT_HIGH
                return

        if self.state == State.BACKWARD:
            return

        elif self.state == State.END:
            pass
        

    def setOutput(self):
        if self.state == self.previous_state:
            return
        print(f"Set Output For State: {self.state}")

        if self.state == State.START:
            self.car.wheels.set_speed(MefControl.INIT_SPEED, acceleration_dt=None)
            self.car.wheels.turn(Wheels.STRAITH_MODE)
            return

        elif self.state == State.STRAIGHT:
            self.car.wheels.turn(Wheels.STRAITH_MODE)
            self.car.wheels.set_speed(MefControl.MAX_SPEED)
            return
       
        elif self.state == State.TURN_LEFT_LOW:
            self.car.wheels.turn(Wheels.LEFT_MODE)

        elif self.state == State.TURN_LEFT_HIGH:
            # self.car.wheels.set_speed(MefControl.HEAVY_TURN, acceleration_dt=0.005)
            self.car.wheels.turn(Wheels.LEFT_HEAVY_MODE)

        elif self.state == State.TURN_RIGHT_LOW:
            self.car.wheels.turn(Wheels.RIGHT_MODE)

        elif self.state == State.TURN_RIGHT_HIGH:
            # self.car.wheels.set_speed(MefControl.HEAVY_TURN, acceleration_dt=0.005)
            self.car.wheels.turn(Wheels.RIGHT_HEAVY_MODE)

        elif self.state == State.SLOWDOWN:
            if self.car.wheels.get_speed() > MefControl.SLOWDOWN_SPEED:
                self.car.wheels.set_speed(MefControl.SLOWDOWN_SPEED, acceleration_dt=0.03)
            else:
                self.car.wheels.set_speed(self.car.wheels.get_speed(), acceleration_dt=None)

        elif self.state == State.STOP:
            self.car.wheels.set_speed(0, acceleration_dt=None)

        elif self.state == State.BACKWARD:
            self.car.wheels.turn(Wheels.STRAITH_MODE)
            self.car.wheels.set_speed(MefControl.BACKWARD_SPEED)

        elif self.state == State.MOVE_AROUND_OBJECT:
            self.car.wheels.set_speed(0, acceleration_dt=None)
            time.sleep(1)
            self.car.wheels.set_speed(40, acceleration_dt=None)
            self.car.wheels.set_angle(45)
            self.car.wheels.set_speed(MefControl.MOVE_AROUND_OBJECT_SPEED, acceleration_dt=0.2)
            time.sleep(2)
            self.car.wheels.set_angle(-45)
            time.sleep(3)
            return

        elif self.state == State.END:
            self.car.wheels.set_speed(0)
            self.car.wheels.set_speed(0, acceleration_dt=None)

    def get_line(self):
        colors = self.car.read_colors()

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