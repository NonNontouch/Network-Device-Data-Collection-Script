from .regular_expression_handler import data_handling
from .error import Error
from time import sleep
from serial import Serial
import serial.tools.list_ports


class serial_connection:
    port: str

    def __init__(self, connection):
        self.username: str = connection.username
        self.password: str = connection.password
        self.enable_password: str = connection.enable_password
        self.timeout: int = connection.timeout
        self.banner_timeout: int = connection.banner_timeout
        self.baudrate: int = connection.banner_timeout
        self.bytesize: int = connection.bytesize
        self.parity: str = connection.parity
        self.stopbits: float = connection.stopbits

    def connect_to_device(self):
        try:
            self.connect = Serial(
                port=self.port,
                timeout=self.timeout,
                baudrate=self.baudrate,
                bytesize=self.bytesize,
                parity=self.parity,
                stopbits=self.stopbits,
            )
            self.connect.open()
        except Exception as e:
            raise e

    def send_command(self, command):
        cmd_output = ""
        self.connect.write(self.to_bytes(command))
        sleep(0.3)
        while True:
            _output = self.get_output()
            cmd_output += _output
            if data_handling.find_prompt(_output):
                break
        if data_handling.check_error(_output):
            raise Error.ErrorCommand(command)

        return cmd_output

    def get_output(self):
        return self.connect.read_all().decode("utf-8")

    def list_serial_ports(self):
        ports = serial.tools.list_ports.comports()
        if ports:
            for port, desc, hwid in sorted(ports):
                print("{}: {} [{}]".format(port, desc, hwid))
            return ports
        else:
            raise Error.NoSerialPortError

    @staticmethod
    def to_bytes(line):
        return f"{line}\n".encode("utf-8")
