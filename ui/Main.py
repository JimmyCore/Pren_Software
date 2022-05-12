import logging
from object_detection.ThreadObjectDetection import ObjectDetection
from vehicle.ThreadVehicle import VehicleControlling
from TinnySim import TinnyK22
from UartWrapper import UARTWrapper
from domain.VehicleEntity import Vehicle


def main():
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
