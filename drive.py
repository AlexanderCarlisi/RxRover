from picarx import Picarx
import time

class CoolerPicarX(Picarx):
    leftMotorSpeed = 0
    rightMotorSpeed = 0
    desiredAngle = 0
    currentAngle = 0
    servoUpdateDebounce = 0.1
    lastUpdate = 0
    cliffDetected = False
    isTeleop = True


    def __init__(self):
        super(CoolerPicarX, self).__init__()


    def drive(self):
        self.set_motor_speed(1, self.leftMotorSpeed)
        self.set_motor_speed(2, -self.rightMotorSpeed)


    def steer(self):
        self.set_dir_servo_angle(self.currentAngle)


    def setAngle(self, newAngle):
        self.desiredAngle = newAngle


    def setWheelSpeeds(self, leftSpeed, rightSpeed):
        self.leftMotorSpeed = leftSpeed
        self.rightMotorSpeed = rightSpeed


    def cliffDetection(self, value):
        self.cliffDetected = value


    def setTeleop(self, value):
        self.isTeleop = value


    def periodic(self):

        if self.cliffDetected:
            self.stop()
            return
        
        if self.isTeleop:
            self.drive()

            # Slowly correct to the desired angle
            if time.time() - self.lastUpdate > self.servoUpdateDebounce:
                if self.currentAngle < self.desiredAngle:
                    self.currentAngle += 1
                elif self.currentAngle > self.desiredAngle:
                    self.currentAngle -= 1
                self.steer()
