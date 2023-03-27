from yolobit import *
from machine import Pin, SoftI2C
import time
from gamepad import *
from robocon import *
from utility import *
from micropython import const
from _thread import start_new_thread

MODE_DPAD = const(1)
MODE_LEFT_JOYSTICK = const(2)
MODE_RIGHT_JOYSTICK = const(3)
MODE_BOTH_JOYSTICK = const(4)


class GamepadHandler():

    def __init__(self):
        #start_new_thread(self.blink_status_led, ())

        self.i2c = SoftI2C(
            scl=Pin(22), sda=Pin(21), freq=100000)

        if self.i2c.scan().count(0x55) == 0:
            self.gamepad = None
            rover.show_rgb_led(0, hex_to_rgb('#ffffff'))
            #self.stop_blink_thread = False
            say('Gamepad Receiver not found')
        else:
            #self.stop_blink_thread = True
            self.gamepad = GamePadReceiver(self.i2c)
            rover.show_rgb_led(0, hex_to_rgb('#0000ff'))
            self.gamepad._verbose = False

            self._speed = 80
            self._speed_turbo = 100

            self.drive_mode = MODE_DPAD
            self.btnChangeMode = 'm2'

            self.btnIncr = 'b'
            self.btnDecr = 'a'

            self.btnTurboMode = None

            self.btnLineFlwMode = None
            self.speedLineFlwMode = 30

            self.colorVal = '#00ff00'
            self.servoVal = [['x1', 'y1', 0, 90], [None, None, None, None]]

            self.btnBallLauncherLoad = None
            self.btnBallLauncherShoot = None
            self.ballLauncherServo1 = 0
            self.ballLauncherServo2 = 1

    def blink_status_led(self):
        status_led_on = 1
        while True:
            if status_led_on:
                rover.show_rgb_led(0, hex_to_rgb('#ffffff'))
            else:
                rover.show_rgb_led(0, hex_to_rgb('#000000'))
            status_led_on = 1 - status_led_on
            time.sleep_ms(100)
            if self.stop_blink_thread:
                rover.show_rgb_led(0, hex_to_rgb('#0000ff'))
                return

    def set_drive_mode(self, drive_mode):
        self.drive_mode = drive_mode

    def set_speed_btn(self, btnIncr='b', btnDecr='a'):
        self.btnIncr = btnIncr
        self.btnDecr = btnDecr

    def set_servo_btn(self, index=0, btn1='x', btn2='y', angle1=0, angle2=90):
        self.servoVal[index][0] = btn1
        self.servoVal[index][1] = btn2
        self.servoVal[index][2] = angle1
        self.servoVal[index][3] = angle2

    def set_ball_launcher_btn(self, index1=0, index2=1, btn1='x', btn2='y'):
        self.ballLauncherServo1 = index1
        self.ballLauncherServo2 = index2
        self.btnBallLauncherLoad = btn1
        self.btnBallLauncherShoot = btn2

    def set_turbo_btn(self, btn='r1'):
        self.btnTurboMode = btn

    def set_change_mode_btn(self, btn='m2'):
        self.btnChangeMode = btn

    def set_follow_line_btn(self, port=0, speed=30, btn=None):
        self.btnLineFlwMode = btn
        self.speedLineFlwMode = speed
        self.portLineFlwMode = port

    def set_led_color(self, color):
        if self.gamepad != None:
            self.colorVal = color
            self.gamepad.set_led_color(hex_to_rgb(self.colorVal))
            rover.show_rgb_led(0, hex_to_rgb(self.colorVal))

    def set_rumble(self, force, duration):
        if self.gamepad != None:
            new_force = translate(force, 0, 100, 0, 255)
            new_duration = translate(duration, 0, 2000, 0, 255)
            self.gamepad.set_rumble(new_force, new_duration)

    def drive_mode_dpad(self):
        if self.gamepad.data['dpad_up'] and self.gamepad.data['dpad_left']:
            rover.move(4)
        elif self.gamepad.data['dpad_up'] and self.gamepad.data['dpad_right']:
            rover.move(2)
        elif self.gamepad.data['dpad_down'] and self.gamepad.data['dpad_left']:
            rover.move(6)
        elif self.gamepad.data['dpad_down'] and self.gamepad.data['dpad_right']:
            rover.move(8)
        elif self.gamepad.data['dpad_up']:
            rover.move(3)
        elif self.gamepad.data['dpad_down']:
            rover.move(7)
        elif self.gamepad.data['dpad_left']:
            rover.move(5)
        elif self.gamepad.data['dpad_right']:
            rover.move(1)
        else:
            rover.stop()

    # 0=left joystick, 1=right joystick
    def drive_mode_single_joystick(self, index=0):

        x, y, angle, dir, distance = self.gamepad.read_joystick(index)

        # speed = distance * self._speed  # adjust speed based on joystick drag distance

        if dir == 2:
            rover.move(4)
        elif dir == 4:
            rover.move(2)
        elif dir == 8:
            rover.move(6)
        elif dir == 6:
            rover.move(8)
        elif dir == 3:
            rover.move(3)
        elif dir == 7:
            rover.move(7)
        elif dir == 1:
            rover.move(5)
        elif dir == 5:
            rover.move(1)
        else:
            rover.stop()

    def drive_mode_both_joystick(self):
        # to be implemented

        j_left = self.gamepad.read_joystick(0)
        j_right = self.gamepad.read_joystick(1)

        new_max_speed_left = translate(j_left[4], 0, 100, 0, rover._speed)
        new_max_speed_right = translate(j_right[4], 0, 100, 0, rover._speed)
        new_max_speed = max(new_max_speed_left, new_max_speed_right)

        if j_left[3] == 3:
            if j_right[3] == 3:
                rover.forward(new_max_speed)
            elif j_right[3] == 7:
                rover.turn_right(new_max_speed/2)
            else:
                rover.set_wheel_speed(new_max_speed_left, 0)

        elif j_left[3] == 7:
            if j_right[3] == 3:
                rover.turn_left(new_max_speed/2)
            elif j_right[3] == 7:
                rover.backward(new_max_speed)
            else:
                rover.set_wheel_speed(-(new_max_speed_left), 0)

        elif j_right[3] == 3:
            if j_left[3] == 3:
                rover.forward(new_max_speed)
            elif j_left[3] == 7:
                rover.turn_left(new_max_speed/2)
            else:
                rover.set_wheel_speed(0, new_max_speed_right)

        elif j_right[3] == 7:
            if j_left[3] == 7:
                rover.backward(new_max_speed)
            elif j_left[3] == 3:
                rover.turn_right(new_max_speed/2)
            else:
                rover.set_wheel_speed(0, -(new_max_speed_right))

        if j_left[3] == 0 and j_right[3] == 0:
            rover.stop()

    def process(self):
        if self.gamepad != None:
            self.gamepad.update()

            if self.gamepad.data[self.btnChangeMode]:
                rover.show_rgb_led(0, hex_to_rgb('#000000'))
                self.drive_mode = (self.drive_mode if isinstance(
                    self.drive_mode, (int, float)) else 0) + 1
                if self.drive_mode > 4:
                    self.drive_mode = 1
                for count in range(self.drive_mode):
                    rover.show_rgb_led(0, hex_to_rgb('#000000'))
                    time.sleep_ms(200)
                    rover.show_rgb_led(0, hex_to_rgb(self.colorVal))
                    time.sleep_ms(200)

            if self.drive_mode == MODE_DPAD:
                self.drive_mode_dpad()
            elif self.drive_mode == MODE_LEFT_JOYSTICK:
                self.drive_mode_single_joystick(0)
            elif self.drive_mode == MODE_RIGHT_JOYSTICK:
                self.drive_mode_single_joystick(1)
            elif self.drive_mode == MODE_BOTH_JOYSTICK:
                self.drive_mode_both_joystick()

            if self.gamepad.data[self.btnIncr]:
                self._speed = (self._speed if isinstance(
                    self._speed, (int, float)) else 0) + 1
                if self._speed > 100:
                    self._speed = 100

            if self.gamepad.data[self.btnDecr]:
                self._speed = (self._speed if isinstance(
                    self._speed, (int, float)) else 0) - 1
                if self._speed < 0:
                    self._speed = 0

            if self.btnTurboMode != None:
                if self.gamepad.data[self.btnTurboMode]:
                    rover._speed = self._speed_turbo
                else:
                    rover._speed = self._speed
            else:
                rover._speed = self._speed

            if self.btnLineFlwMode != None:
                if self.gamepad.data[self.btnLineFlwMode]:
                    follow_line(self.speedLineFlwMode)

            if (self.btnBallLauncherLoad != None) or (self.btnBallLauncherShoot != None):
                if self.gamepad.data[self.btnBallLauncherLoad]:
                    time.sleep_ms(250)
                    ball_launcher(self.ballLauncherServo1,
                                  self.ballLauncherServo2, mode=0)

                if self.gamepad.data[self.btnBallLauncherShoot]:
                    time.sleep_ms(250)
                    ball_launcher(self.ballLauncherServo1,
                                  self.ballLauncherServo2, mode=1)

            for i in range(2):
                if self.servoVal[i][0] != None:
                    if self.gamepad.data[self.servoVal[i][0]]:
                        rover.servo_write(i+1, self.servoVal[i][2])
                    if self.gamepad.data[self.servoVal[i][1]]:
                        rover.servo_write(i+1, self.servoVal[i][3])

            # print('Mode: ',self.drive_mode ,'Speed: ', rover._speed)
            # If it's < 120, when you click button some activities be duplicated.
            time.sleep_ms(120)


gamepad_handler = GamepadHandler()
