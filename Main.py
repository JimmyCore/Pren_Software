import logging
from ThreadObjectDetection import ObjectDetection
from ThreadVehicle import VehicleControlling
from TinnySim import TinnyK22
from UartWrapper import UARTWrapper
from VehicleEntity import Vehicle

import RPi.GPIO as GPIO

"""
GPIO PINS
Notaus: GPIO 19
Startknopf: GPIO 27
"""


def main():
    while True:



        try:
            logging.info("Start Program...")
            vehicle = Vehicle()
            uart = UARTWrapper()
            controlling = VehicleControlling(vehicle=vehicle, uart_wrapper=uart)
            object_det = ObjectDetection(controlling)
            object_det.run()
            tinny = TinnyK22(uart_buffer=uart)
            controlling.run()
            tinny.run()
        except KeyboardInterrupt:
            pass
            # stop_timer()
if __name__ == '__main__':
    main()
