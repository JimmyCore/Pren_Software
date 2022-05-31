import threading
from VehicleActionEnum import VehicleAction

SENSOR_KEYS = ['speed', 'voltage_print', 'coils', 'acceleration', 'voltage_motor']


class Vehicle:

    def __init__(self):
        self.STATE_LOCK = threading.Lock()
        with self.STATE_LOCK:
            self.state = VehicleAction.STOP

    def drive_action(self, action: VehicleAction):
        self.state = action

    def get_state(self):
        return self.state

    def set_state(self, new_state):
        self.state = new_state

    def isDriving(self) -> bool:
        if self.state is VehicleAction.FULL_SPEED:
            return True
        else:
            return False
