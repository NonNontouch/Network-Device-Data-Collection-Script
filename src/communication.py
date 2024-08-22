from .ssh_module import ssh_connection as ssh
from .telnet_module import telnet_connection as telnet
from .serial_module import serial_connection as serial
from .regular_expression_handler import data_handling as data_handling
from .error import Error as Error

import re as re
import paramiko as para


class connection:
    # Common variable
    hostname: str
    username: str
    password: str
    enable_password: str = ""
    timeout: float = 4
    banner_timeout: int = 4
    port: int = None
    # Serial Variable
    baudrate: int
    bytesize: int
    parity: str
    stopbits: float
    common_baudrate = [
        50,
        75,
        110,
        134,
        150,
        200,
        300,
        600,
        1200,
        1800,
        2400,
        4800,
        9600,
        19200,
        28800,
        38400,
        57600,
        76800,
        115200,
        230400,
        460800,
        576000,
        921600,
    ]
    connection = None

    def set_hostname(self, hostname: str):
        self.hostname = hostname

    def set_port(self, port: int):
        if port >= 65545 or port < 1:
            return
        self.port = port

    def set_username(self, username: str):
        self.username = username

    def set_password(self, password: str):
        self.password = password

    def set_enable_password(self, enable_password: str):
        self.enable_password = enable_password

    def set_timeout(self, timeout: float):
        if timeout <= 0:
            return
        self.timeout = timeout

    def set_banner_timeout(self, banner_timeout: int):
        if banner_timeout < 0:
            return
        self.banner_timeout = banner_timeout

    def set_baudrate(self, baudrate: int):
        if baudrate not in self.common_baudrate:
            return
        self.baudrate = baudrate

    def set_bytesize(self, bytesize: int):
        if bytesize < 0:
            return
        self.bytesize = bytesize

    def set_parity(self, parity: str):
        self.parity = parity

    def set_stopbits(self, stopbits: float):
        if stopbits < 0:
            return
        self.stopbits = stopbits
    

    def set_ssh_connection(self):
        self.connection = ssh(self)
        try:
            self.connection.connect_to_device()
        except OSError as e:
            print(e)
            self.connection = None
        except para.SSHException as e:
            print(e)
            self.connection = None
        except Exception as e:
            print(f"Error connecting to SSH: {e}")
            self.connection = None

    def set_telnet_connection(self):
        if self.port == None:
            self.port = 23
        self.connection = telnet(self)
        try:
            self.connection.connect_to_device()
            self.connection.login()
        except Exception as e:
            print(f"Error connecting to Telnet: {e}")
            self.connection = None

    def set_serial_connection(self):
        self.connection = serial(self)
        try:
            self.connection.connect_to_device()
            # self.connection.login()
        except Exception as e:
            print(f"Error connecting to Serial: {e}")
            self.connection = None

    def send_list_command(self, command_list_json: dict = {}):
        if self.connection == None:
            raise Error.ConnectionError
        if self.connection.is_enable() is False:
            self.connection.enable_device(
                enable_command=command_list_json["Enable Device"],
                password=self.enable_password,
            )
        command_list_json.pop("Enable Device")
        # command_list_json.pop("show vlt status")
        # command_list_json.pop("show vlt number")
        command_list_json.pop("show tech-support")

        command_list = list(command_list_json.values())
        command_list_json = list(command_list_json.keys())
        try:
            result: dict = {}
            for i in range(len(command_list_json)):
                command = command_list[i]
                result[command_list_json[i]] = data_handling.remove_control_char(
                    self.connection.send_command(command)
                )
            for i in result.values():
                print(i)
            return result

        except Error.ErrorCommand as e:
            print(e)
            return None

    def get_vlt_number(self, command_json: dict):
        self.connection.send_command("")
        raw_vlt_num = self.connection.send_command(command_json["show vlt number"])
        match = re.search(r"vlt-domain (\d+)", raw_vlt_num)
        if match:
            return int(match.group(1))
        else:
            return None
