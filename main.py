from drive import CoolerPicarX
from control import Controls
from cliffDetection import CliffDetection
from ultrasonic import USSensor
from camera import Camera
from audio import Audio
from autonomous import DistancePIDAuto
import pygame

def main():
    pygame.init()
    screen = pygame.display.set_mode([500, 500])

    picarx = CoolerPicarX()
    controller = Controls(picarx)
    # cliffDetection = CliffDetection(picarx)
    sonicSensor = USSensor(picarx)
    camera = Camera(picarx)
    audio = Audio(camera)
    running = True

    auto = DistancePIDAuto(picarx, sonicSensor)

    while running:
        controller.periodic()
        # cliffDetection.periodic()
        picarx.periodic()
        camera.periodic()
        audio.periodic()

        if picarx.isTeleop:
            sonicSensor.teleopPeriodic()
        else:
            auto.periodic()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                picarx.stop()

    pygame.quit()

if __name__ == "__main__":
    main()
