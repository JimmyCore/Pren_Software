import collections
import threading


class UARTWrapper:
    def __init__(self):
        self.port_lock = threading.Lock()
        self.send_message_lock = threading.Lock()
        self.read_message_lock = threading.Lock()
        with self.port_lock:
            self.open_flag = False
        with self.send_message_lock:
            self.send_message_buffer = collections.deque(maxlen=100)
        with self.read_message_lock:
            self.read_message_buffer = collections.deque(maxlen=100)

    def writeRaspberry(self, message):
        # print(f"{threading.current_thread().getName()}: Write {message} to Buffer.")
        self.read_message_buffer.append(message)

    def writeTiny(self, message):
        # print(f"{threading.current_thread().getName()}: Write {message} to Buffer.")
        self.send_message_buffer.append(message)

    def readRaspberry(self):
        if self.RaspIsEmpty():
            return ""
        return str(self.send_message_buffer.pop())

    def readTiny(self):
        if self.TinyIsEmpty():
            return ""
        return str(self.read_message_buffer.pop())

    def RaspIsEmpty(self):
        return len(self.send_message_buffer) == 0

    def TinyIsEmpty(self):
        return len(self.read_message_buffer) == 0

    def isOpen(self):
        return self.open_flag

    def open(self):
        self.open_flag = True

    def close(self):
        self.open_flag = False
