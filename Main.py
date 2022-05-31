import logging
from ThreadObjectDetection import ObjectDetection
from ThreadVehicle import VehicleControlling
from TinnySim import TinnyK22
from UartWrapper import UARTWrapper
from VehicleActionEnum import VehicleAction
from VehicleEntity import Vehicle

import RPi.GPIO as GPIO

"""
GPIO PINS
Notaus: GPIO 19
Startknopf: GPIO 27
"""
NOT_AUS = 19
START = 27


def main():
    PROGRAM_STARTED = False
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(NOT_AUS, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(START, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    logging.info("Start Program...")
    vehicle = Vehicle()
    uart = UARTWrapper()
    controlling = VehicleControlling(vehicle=vehicle, uart_wrapper=uart)
    object_det = ObjectDetection(controlling)

    while True:
        if GPIO.input(NOT_AUS):
            controlling.OnDrive(VehicleAction.STOP)
            PROGRAM_STARTED = False
            break
        elif GPIO.input(START) and not PROGRAM_STARTED:
            try:      
                object_det.run()
                controlling.run()
                controlling.OnDrive(VehicleAction.FULL_SPEED)
            except KeyboardInterrupt:
                pass
            # stop_timer()
            PROGRAM_STARTED = True

        elif GPIO.input(START) and PROGRAM_STARTED:
            controlling.OnDrive(VehicleAction.STOP)
            PROGRAM_STARTED = False


if __name__ == '__main__':
    main()
