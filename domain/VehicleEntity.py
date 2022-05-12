import threading
from collections import namedtuple

from domain.VehicleActionEnum import VehicleAction

SENSOR_KEYS = ['speed', 'voltage_print', 'coils', 'acceleration', 'voltage_motor']


class Vehicle:

    def __init__(self):
        self.STATE_LOCK = threading.Lock()
        self.DATA_LOCK = threading.Lock()

        with self.STATE_LOCK:
            self.state = VehicleAction.STOP

        with self.DATA_LOCK:
            # 5 Voltage, Supply Voltage, Motoren Strom,
            # Beschleunigung x, Beschleunigung y, Beschleunigung z, Motor Speed rpm,
            # Spannung Spule 2, 3 = Regelung, Spannung Spule 1, 4 = Reserve,
            # Encoder Lichtschranke
            self.sensor_data = namedtuple("Sensor", "speed voltage_print coils acceleration voltage_motor")

    def drive_action(self, action: VehicleAction):
        self.state = action

    def update(self, new_data):
        self.sensor_data = new_data

    def get_state(self):
        return self.state

    def set_state(self, new_state):
        self.state = new_state

    def isDriving(self) -> bool:
        if self.state is VehicleAction.Driving:
            return True
        else:
            return False
