from .regular_expression_handler import data_handling
from .error import Error
from time import sleep
from serial import Serial
import serial.tools.list_ports


class serial_connection:
    def __init__(self):

        # self.username: str = connection.username
        # self.password: str = connection.password
        # self.enable_password: str = connection.enable_password
        # self.timeout: int = connection.timeout
        # self.banner_timeout: int = connection.banner_timeout
        return

    def connect_to_device(self):
        self.connect = Serial()

    def list_serial_ports(self):
        """Lists all available serial ports."""
        ports = serial.tools.list_ports.comports()
        if ports:
            for port in ports:
                print(f"Port: {port.device}")
        else:
            print("No serial ports found")


test = serial_connection()
test.list_serial_ports()
