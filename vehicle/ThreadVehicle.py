import logging
import threading
from web_service import DataCommunication as dc
from collections import namedtuple

# import serial

from threading import Thread
from time import sleep
from typing import Any

from UartWrapper import UARTWrapper
from domain.VehicleEntity import Vehicle
from domain.VehicleActionEnum import VehicleAction

logging.basicConfig(filename="../vehicleLog.log", level=logging.ERROR)


class VehicleControlling(Thread):
    def __init__(self, vehicle: Vehicle, uart_wrapper: UARTWrapper):
        super().__init__()

        self.UART_LOCK = threading.Lock()
        self.ACTION_LOCK = threading.Lock()

        self.drive_event = threading.Event()

        self.vehicle = vehicle
        # self.ser = serial.Serial('/dev/ttyS1', 9600)
        self.ser = uart_wrapper
        dc.start_client_productive()
        # dc.start_client_local()
        # dc.start_timer()
        dc.event_to_server("debug", "main final started")

    def OnDrive(self, action: VehicleAction):
        self.vehicle.drive_action(action)
        self.drive_event.set()

    def drive_action(self) -> Any:
        self.drive_event.wait()
        self.drive_vehicle()
        self.drive_event.clear()
        self.drive_action()

    def drive_vehicle(self):
        # print(f"{threading.current_thread().getName()}: Try to Drive Car with {self.vehicle.get_state()}")
        # print(f"Car drive action: {self.vehicle.state}")
        self.uart(action="write", event=self.vehicle.state)

    def uart(self, action: str, event: str = "") -> Any:
        with self.UART_LOCK:
            if not self.ser.isOpen():
                self.ser.open()
            if action == "read":
                # ans = self.ser.read().decode("utf-8")
                ans = self.ser.readRaspberry()
                self.ser.close()
                return ans
            elif action == "write":
                self.ser.writeRaspberry(event)
                self.ser.close()
                return
            else:
                self.ser.close()
                raise ValueError(f"Action {action} is not available.")

    def read_tinny_uart_data(self, timout_sec=5):
        while True:
            data = self.uart("read")
            if len(data) == 0:
                sleep(timout_sec)
                continue
            else:
                unpacked = VehicleControlling.unpack_sensor_data(data)
                self.send_sensor_data_to_server(unpacked)
            sleep(timout_sec)

    def send_sensor_data_to_server(self, unpacked):
        fields = list(unpacked._fields)
        # print(f'fields is: {fields}')
        for field in fields:
            # print(f'attributes sending: {field, getattr(unpacked, field)}')
            dc.update_sensor_data(field, getattr(unpacked, field))

    def drive_random_car(self):
        while True:
            sleep(10)
            self.OnDrive(VehicleAction.HALF_SPEED.value)

    @staticmethod
    def update_plant_website(plant):
        common_n1 = "Common Name 1"
        common_n2 = "Common Name 2"
        common_n3 = "Common Name 3"
        if len(plant.commonNames) >= 1:
            common_n1 = plant.commonNames[0]
        if len(plant.commonNames) >= 2:
            common_n2 = plant.commonNames[1]
        if len(plant.commonNames) >= 3:
            common_n3 = plant.commonNames[2]

        dc.update_sensor_data('plant_data', {
            "position": f"{plant.position}",
            "genus": f"{plant.genus}",
            "family": f"{plant.family}",
            "scientificName": f"{plant.scientificName}",
            "commonNames": [f"{common_n1}", f"{common_n2}", f"{common_n3}"]
        })

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
        thread_vehicle_data = Thread(target=self.read_tinny_uart_data, name="Tinny-Data-Thread")
        thread_vehicle_data.start()
        thread_vehicle_action = Thread(target=self.drive_random_car, name="Random-Drive-Thread")
        thread_vehicle_action.start()
