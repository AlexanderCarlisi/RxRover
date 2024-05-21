class DistancePIDAuto:

    picarx = None
    USSensor = None
    desiredDistance = 2
    previousError = 0
    tolerance = 0.5
    kP = 1
    kD = 0.01
    checks = 0

    def __init__(self, _picarx, _USSensor):
        self.picarx = _picarx
        self.USSensor = _USSensor

    def periodic(self):
        distance = self.USSensor.getDistance()
        print(distance)

        if abs(distance - self.desiredDistance) < self.tolerance:
            self.checks += 1
            return
        
        if self.checks > 5:
            self.picarx.setWheelSpeeds(0, 0)
            self.picarx.drive()
            return

        speed = 0

        # proportional
        error = distance - self.desiredDistance
        speed += self.kP * error

        # derivative
        speed += self.kD * (error - self.previousError)
        self.previousError = error

        self.picarx.setWheelSpeeds(speed, speed)
        self.picarx.drive()
