import time
from threading import Thread
from picar.back_wheels import Back_Wheels as BackWheels;
from picar.front_wheels import Front_Wheels as FrontWheels;

class Wheels:
    TURNING_ANGLE_HEAVY = 45
    TURNING_ANGLE_LOW = 5
    DIFFERANTIAL_FACTOR = 0.5

    DEFFAULT_SPEED_ACCELERATION_DT = 0.1
    DEFFAULT_ANGLE_ACCELERATION_DT = 0.005

    STRAITH_MODE = 1
    LEFT_MODE = 2
    LEFT_HEAVY_MODE = 3
    RIGHT_MODE = 4
    RIGHT_HEAVY_MODE = 5

    def __init__(self):
        self._back_wheel = BackWheels()
        self._front_wheel = FrontWheels()

        self._speed = 0
        self._angle = 0

        self._speed_thread_exit_flag = False
        self._speed_thread = None

        self._angle_thread_exit_flag = False
        self._angle_thread = None

        self._diff_left_factor = 1
        self._diff_right_factor = 1

    def set_speed(self, new_speed, acceleration_dt=DEFFAULT_SPEED_ACCELERATION_DT):
        new_speed = round(new_speed)
        self._set_speed_threaded(new_speed, acceleration_dt)

    def get_speed(self):
        return self._speed

    def set_angle(self, new_angle, acceleration_dt=DEFFAULT_ANGLE_ACCELERATION_DT, left_factor=1, right_factor=1):
        new_angle = round(new_angle)
        self._set_angle_threaded(new_angle, acceleration_dt)
        self._set_differential(left_factor, right_factor)

    def turn(self, mode, acceleration_dt=None):
        if mode == Wheels.STRAITH_MODE:
            correction = -8
            self.set_angle(0 + correction, acceleration_dt)
            self._set_differential()

        elif mode == Wheels.LEFT_MODE:
            self.set_angle(Wheels.TURNING_ANGLE_LOW, acceleration_dt)
            self._set_differential()
        
        elif mode == Wheels.LEFT_HEAVY_MODE:
            self.set_angle(Wheels.TURNING_ANGLE_HEAVY, acceleration_dt)
            self._set_differential(left_factor=Wheels.DIFFERANTIAL_FACTOR)
        
        elif mode == Wheels.RIGHT_MODE:
            correction = -15
            self.set_angle(-Wheels.TURNING_ANGLE_LOW + correction, acceleration_dt)
            self._set_differential()
        
        elif mode == Wheels.RIGHT_HEAVY_MODE:
            self.set_angle(-Wheels.TURNING_ANGLE_HEAVY, acceleration_dt)
            self._set_differential(right_factor=Wheels.DIFFERANTIAL_FACTOR)

    def _set_differential(self, left_factor=1, right_factor=1):
        self._diff_left_factor = left_factor
        self._diff_right_factor = right_factor
        self._back_wheel.left_wheel.speed = int(left_factor * self._speed)
        self._back_wheel.right_wheel.speed = int(right_factor * self._speed)

    # SPEED SECTION
    def _set_speed_threaded(self, new_speed, acceleration_dt):            
        if self._speed_thread is not None:
            self._speed_thread_exit_flag = True
            self._speed_thread.join()
        self._speed_thread_exit_flag = False
        self._speed_thread = Thread(target=self._speed_thread_target, args=[new_speed, acceleration_dt])
        self._speed_thread.start()

    def _speed_thread_target(self, new_speed, acceleration_dt):
        def set_speed(speed):
            if (speed >= 0): self._back_wheel.forward()
            else: self._back_wheel.backward()
            self._speed = abs(speed)
            self._back_wheel.left_wheel.speed = int(self._diff_left_factor * self._speed)
            self._back_wheel.right_wheel.speed = int(self._diff_right_factor * self._speed)

        if acceleration_dt is not None:
            start_speed = self._speed
            step = (1 if new_speed > start_speed else -1) * 3
            for s in range(start_speed, new_speed, step):
                set_speed(s)
                for _ in range(32):
                    time.sleep(acceleration_dt / 32)
                    if self._speed_thread_exit_flag: return
        else:
            set_speed(new_speed)
    # END SPEED SECTION

    # ANGLE SECTION
    def _set_angle_threaded(self, new_angle, acceleration_dt):
        if self._angle_thread is not None:
            self._angle_thread_exit_flag = True
            self._angle_thread.join()
        self._angle_thread_exit_flag = False
        self._angle_thread = Thread(target=self._angle_thread_target, args=[new_angle, acceleration_dt])
        self._angle_thread.start()


    def _angle_thread_target(self, new_angle, acceleration_dt):
        def set_angle(angle):
            self._angle = angle
            self._front_wheel.turn(90 - self._angle)

        if acceleration_dt is not None:
            start_angle = self._angle
            step = 1 if new_angle > start_angle else -1
            for a in range(start_angle, new_angle, step):
                set_angle(a)
                for _ in range(32):
                    time.sleep(acceleration_dt / 32)
                    if self._angle_thread_exit_flag: return
                
        else:
            set_angle(new_angle)
    # END ANGLE SECTION


