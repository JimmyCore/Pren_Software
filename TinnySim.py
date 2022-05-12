import random
from threading import Thread
from time import sleep

from UartWrapper import UARTWrapper


class TinnyK22(Thread):
    def __init__(self, uart_buffer: UARTWrapper):
        super().__init__()
        self.uart_buffer = uart_buffer

    def random_sensor_data(self):
        pass

    def read_raspberry_commands(self):
        pass
        # print("Read Raspberry Command: ", self.uart_buffer.readTiny())

    def run(self):
        while True:
            data = ""
            for i in range(10):
                data += str(random.choice(range(100))) + ";"
            data = data[:-1]
            # data = "0;1;2;2;2;2;3;3;3;4"
            self.uart_buffer.writeTiny(data)
            self.read_raspberry_commands()
            sleep(0)
