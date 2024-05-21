#import tty
#import sys
#import termios
import pygame
import time


class Controls:
    picarx = None
    orig_settings = None
    speed = 50 # out of 100%
    controller = None

    # Needed to prevent Servos from failing
    steerDirection = 0 # 0 is straight, -1 is left, 1 is right

    # Prevent Servos from almost breaking and giving me a heart attack
    steerDebounce = 1.5
    previousSteerTime = 0

    controllerDeadzone = 0.3


    def __init__(self, _picarx):
        #self.orig_settings = termios.tcgetattr(sys.stdin)
        #tty.setcbreak(sys.stdin)
        self.picarx = _picarx
        try:
            self.controller = pygame.joystick.Joystick(0)
            self.controller.init()
        except:
            pass


    def drive(self, modifier=1):
        if not self.picarx.isTeleop: 
            return
        self.picarx.setWheelSpeeds(self.speed * modifier, self.speed * modifier)


    # Positive modifier is counterclockwise, negative is clockwise
    def rotate(self, modifier=1):
        if not self.picarx.isTeleop:
            return
        self.picarx.setWheelSpeeds(self.speed * -modifier, self.speed * modifier)

    # Positive is left
    def steer(self, modifier=1):
        if self.steerDirection == modifier or time.time() - self.previousSteerTime < self.steerDebounce or not self.picarx.isTeleop:
            return
        self.previousSteerTime = time.time()
        self.steerDirection = modifier
        self.picarx.setAngle(-60 * modifier)


    def periodic(self):
        if self.picarx.isTeleop:
            self.picarx.setWheelSpeeds(0, 0)

        # Controller Input
        if self.controller is not None:
            # Left Stick
            if abs(self.controller.get_axis(pygame.CONTROLLER_AXIS_LEFTY)) > self.controllerDeadzone:
                self.drive(-self.controller.get_axis(1))
            if abs(self.controller.get_axis(pygame.CONTROLLER_AXIS_LEFTX)) > self.controllerDeadzone:
                self.rotate(-self.controller.get_axis(0))

            # D-Pad
            if (self.controller.get_button(pygame.CONTROLLER_BUTTON_DPAD_LEFT)):
               self.steer()
            elif (self.controller.get_button(pygame.CONTROLLER_BUTTON_DPAD_RIGHT)):
               self.steer(-1)
            elif (self.controller.get_button(pygame.CONTROLLER_BUTTON_DPAD_UP)):
               self.steer(0)


        # Keyboard Input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.drive()
        elif keys[pygame.K_s]:
            self.drive(-1)

        if keys[pygame.K_a]:
            self.steer()
        elif keys[pygame.K_d]:
            self.steer(-1)

        if keys[pygame.K_q]:
            self.rotate()
        elif keys[pygame.K_e]:
            self.rotate(-1)

        if keys[pygame.K_SPACE]:
            self.picarx.setAngle(0)
            self.picarx.stop()

        if keys[pygame.K_1]:
            self.picarx.setTeleop(True)
        elif keys[pygame.K_2]:
            self.picarx.setTeleop(False)
