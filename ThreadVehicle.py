import logging
import threading
import DataCommunication as dc
from collections import namedtuple
import serial
from threading import Thread
from time import sleep
from typing import Any
from UartWrapper import UARTWrapper
from VehicleEntity import Vehicle
from VehicleActionEnum import VehicleAction

logging.basicConfig(filename="vehicleLog.log", level=logging.ERROR)


class VehicleControlling(Thread):
    def __init__(self, vehicle: Vehicle, uart_wrapper: UARTWrapper):
        super().__init__()

        self.UART_LOCK = threading.Lock()
        self.ACTION_LOCK = threading.Lock()
        self.drive_event = threading.Event()
        self.vehicle = vehicle

    def OnDrive(self, action: VehicleAction):
        self.vehicle.drive_action(action)
        self.drive_event.set()

    def drive_action(self) -> Any:
        self.drive_event.wait()
        self.drive_vehicle()
        self.drive_event.clear()
        self.drive_action()

    def drive_vehicle(self):
        self.uart(action="write", event=self.vehicle.state.value)

    def uart(self, action: str, event: str = "") -> Any:
        with self.UART_LOCK:
            with serial.Serial('/dev/ttyS0', 9600, timeout=1) as ser:
                if action == "read":
                    sensor_data = ser.readline().decode("utf-8")
                    dc.event_to_server("debug", f"Read Sensor Data from Tinny: {sensor_data}")
                    return sensor_data
                elif action == "write":
                    dc.event_to_server("debug", f"Send {event} Command to Tinny")
                    ser.write(event)
                    return
                else:
                    raise ValueError(f"Action {action} is not available.")

    def read_tinny_uart_data(self, timout_sec=5):
        while True:
            data = self.uart("read")
            if len(data) <= 5:
                sleep(timout_sec)
                continue
            else:
                unpacked = VehicleControlling.unpack_sensor_data(data)
                self.send_sensor_data_to_server(unpacked)
            sleep(timout_sec)

    def drive_random_car(self):
        while True:
            sleep(10)
            self.OnDrive(VehicleAction.HALF_SPEED.value)

    def send_sensor_data_to_server(self, unpacked):
        fields = list(unpacked._fields)
        for field in fields:
            dc.event_to_server("debug", f'attributes sending: {field, getattr(unpacked, field)} to Website')
            dc.send_data_update(field, getattr(unpacked, field))

    @staticmethod
    def update_similar_plant_on_webseite(same_plant_pos):
        dc.send_data_update("match_found", same_plant_pos)

    @staticmethod
    def unpack_sensor_data(data: str):
        data_lst = data.split(";")
        # Keys: ['speed', 'voltage_print', 'coils', 'acceleration', 'voltage_motor']
        unpacked = namedtuple("Sensor", "speed voltage_print coils acceleration voltage_motor")

        unpacked.speed = float(data_lst[0])
        unpacked.voltage_print = float(data_lst[1])

        coils = [
            {"nr_coil": 1, "value": 0.0},
            {"nr_coil": 2, "value": 0.0},
            {"nr_coil": 3, "value": 0.0},
            {"nr_coil": 4, "value": 0.0}
        ]

        accelerations = [
            {"axis": "x", "value": 0.0},
            {"axis": "y", "value": 0.0},
            {"axis": "z", "value": 0.0}
        ]

        for index, sensor in enumerate(data_lst[2:6]):
            coils[index]["value"] = float(sensor)

        for index, sensor in enumerate(data_lst[6:9]):
            accelerations[index]["value"] = float(sensor)

        unpacked.coils = coils
        unpacked.acceleration = accelerations
        unpacked.voltage_motor = float(data_lst[-1])

        return unpacked

    def run(self):
        thread_driving = Thread(target=self.drive_action, name="Driving-Thread")
        thread_driving.start()
