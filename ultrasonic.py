from time import sleep

class USSensor:
    picarx = None
    teleopSaveDistance = -1 # Disabled

    def __init__(self, _picarx):
        self.picarx = _picarx

    def getDistance(self):
        return round(self.picarx.ultrasonic.read(), 2)
    
    def teleopPeriodic(self):
        distance = self.getDistance()
        print(distance)
        if distance < self.teleopSaveDistance and distance > -1:
            self.picarx.setTeleop(False)
            self.picarx.setWheelSpeeds(-100, -100)
            self.picarx.drive()
            sleep(0.1)
            self.picarx.setWheelSpeeds(0, 0)
            self.picarx.drive()
            self.picarx.setTeleop(True)
