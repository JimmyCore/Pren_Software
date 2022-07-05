import logging
import DataCommunication as dc
from ThreadObjectDetection import ObjectDetection
from ThreadVehicle import VehicleControlling
from UartWrapper import UARTWrapper
from VehicleActionEnum import VehicleAction
from VehicleEntity import Vehicle
import RPi.GPIO as GPIO
import time

NOT_AUS = 19
START = 27


def main():
    PROGRAM_STARTED = False
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(NOT_AUS, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(START, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    logging.info("Start Program...")

    dc.start_client_productive()
    dc.event_to_server("debug", "main final started")

    vehicle = Vehicle()
    uart = UARTWrapper()
    controlling = VehicleControlling(vehicle=vehicle, uart_wrapper=uart)
    object_det = ObjectDetection(controlling)

    try:
        while True:
            if not GPIO.input(START) and not PROGRAM_STARTED:
                print("Start CAR")
                object_det.run()
                controlling.run()
                controlling.OnDrive(VehicleAction.FULL_SPEED)
                dc.start_timer()
                PROGRAM_STARTED = True
                time.sleep(5)

            elif not GPIO.input(START) and PROGRAM_STARTED:
                print("Stop Car")
                controlling.OnDrive(VehicleAction.STOP)
                PROGRAM_STARTED = False
                time.sleep(5)
    except KeyboardInterrupt:
        dc.stop_timer()
    finally:
        dc.stop_timer()


if __name__ == '__main__':
    main()
