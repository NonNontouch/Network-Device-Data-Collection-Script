from .ssh_module import ssh_connection as ssh
from .telnet_module import telnet_connection as telnet
from .serial_module import serial_connection as serial
from .regular_expression_handler import data_handling as data_handling
import src.error as Error

import re as re
import paramiko as para


class connection_manager:
    """_Facade class that used to control ssh,telnet and serial._"""

    # Common variable with default value
    hostname: str = ""
    username: str = ""
    password: str = ""
    enable_password: str = ""
    # TCP timeout
    timeout: float = 4
    # Login timeout
    login_wait_time: float = 3
    # Banner Timeout
    banner_timeout: float = 15
    # Command timeout
    command_retriesdelay: float = 4
    # Command retry time
    command_maxretries: int = 4
    port: int = None
    # Serial Variable with default value
    serial_port: str = ""
    serial_port_list: list
    baudrate: int = 115200
    bytesize: int = 8
    parity: str = "N"
    stopbits: float = 1
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
        """Set the device hostname, which can be an IP address or a resolvable hostname.

        Args:
            hostname (str): The IP address or hostname to set as the device's hostname.
        """
        self.hostname = hostname

    def set_port(self, port: int):
        """Set the device port.

        The port must be within the range of 1 to 65544; otherwise, it will retain the previous value or default value.

        Args:
            port (int): The port number to set for the device.
        """
        self.port = port if 1 <= port < 65545 else self.port

    def set_username(self, username: str):
        """Set the username for device access.

        Args:
            username (str): The username to authenticate with the device.
        """
        self.username = username

    def set_password(self, password: str):
        """Set the password for device access.

        Args:
            password (str): The password to authenticate with the device.
        """
        self.password = password

    def set_enable_password(self, enable_password: str):
        """Set the enable password for privileged mode access on the device.

        Args:
            enable_password (str): The password required to enter privileged mode.
        """
        self.enable_password = enable_password

    def set_timeout(self, timeout: float):
        """Set the timeout for device operations.

        The timeout must be greater than 0; otherwise, it will retain the previous value or default value.

        Args:
            timeout (float): The timeout duration in seconds for device operations.
        """
        self.timeout = timeout if timeout > 0 else self.timeout

    def set_login_wait_time(self, login_wait_time: float):
        """Set the wait time for login operations.

        The wait time must be non-negative; otherwise, it will retain the previous value or default value.

        Args:
            login_wait_time (float): The wait time in seconds for login operations.
        """
        self.login_wait_time = (
            login_wait_time if login_wait_time >= 0 else self.login_wait_time
        )

    def set_command_retries_delay(self, command_retriesdelay: float):
        """Set the wait time for command execution.

        The wait time must be non-negative; otherwise, it will retain the previous value or default value.

        Args:
            command_wait_time (float): The wait time in seconds for command execution.
        """
        self.command_retriesdelay = (
            command_retriesdelay
            if command_retriesdelay >= 0
            else self.command_retriesdelay
        )

    def set_banner_timeout(self, banner_timeout: int):
        """Set the timeout duration for banner display.

        The banner timeout must be non-negative; otherwise, it will retain the previous value or default value.

        Args:
            banner_timeout (int): The timeout duration in seconds for banner display.
        """
        self.banner_timeout = (
            banner_timeout if banner_timeout >= 0 else self.banner_timeout
        )

    def set_command_maxretries(self, command_maxretries: int):
        """Set the maximum number of retries for command execution.

        The maximum retries must be non-negative; otherwise, the previous value will be retained.

        Args:
            command_maxretries (int): The maximum number of retries to set for command execution.
        """
        self.command_maxretries = (
            command_maxretries if command_maxretries >= 0 else self.command_maxretries
        )

    def set_baudrate(self, baudrate: int):
        """Set the baud rate for serial communication.

        The baud rate must be one of the common baud rates; otherwise, it will retain the previous value or default value.

        Args:
            baudrate (int): The baud rate for serial communication.
        """
        self.baudrate = baudrate if baudrate in self.common_baudrate else self.baudrate

    def set_bytesize(self, bytesize: int):
        """Set the byte size for serial communication.

        The byte size must be non-negative; otherwise, it will retain the previous value or default value.

        Args:
            bytesize (int): The byte size for serial communication.
        """
        self.bytesize = bytesize if bytesize >= 0 else self.bytesize

    def set_parity(self, parity: str):
        """Set parity variable

        Args:
            parity (str): _parity_ _bit_
        """
        self.parity = parity

    def set_stopbits(self, stopbits: float):
        """
        Funcitons:
            Set stopbits variable

        Arguments:
            NoSerialPortError: If no serial ports are found.
        """

        self.stopbits = stopbits if stopbits >= 0 else self.stopbits

    def set_ssh_connection(self):
        """
        Set connection variable to ssh and then try to connect to the device

        Raises:
            OSError: If socket error
            SSHException: If authentication fail
            Exception: If unknown exception is founded
        """
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
        """Set connection as telnet and try connect and login to it"""
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
        """
        Set connection as serial and try connect and login to it
        """
        self.connection = serial(self)
        try:
            self.connection.set_serial_object()
            print(self.get_serial_port())
            self.connection.connect_to_device(self.serial_port_list[2])
            self.connection.login()
        except Exception as e:
            print(f"Error connecting to Serial: {e}")
            self.connection = None

    def get_serial_port(self):
        """_Get list of all avaiable serial port in computer._"""
        if isinstance(self.connection, serial):
            self.serial_port_list = self.connection.list_serial_ports()
            return self.serial_port_list

    def send_list_command(self, command_dict_json: dict):
        """_Send command to device from sequnce given in dict argument._

        Args:
            command_list_json (dict): _A dict variable which contain command template._

        Raises:
            Error.ConnectionError: _If connection is None, Functino will raise this error._

        Returns:
            dict: _A dict of command result from given command._
        """
        result: dict = {}
        if self.connection == None:
            raise Error.ConnectionError
        try:
            if self.connection.is_enable() is False:
                if "Enable Device" in command_dict_json:
                    self.connection.enable_device(
                        enable_command=command_dict_json["Enable Device"],
                        password=self.enable_password,
                    )
                    del command_dict_json["Enable Device"]
                else:
                    raise Error.LoginError("Program can't enable device")
            else:
                pass
        except (
            Error.ErrorCommand,
            Error.ConnectionLossConnect,
            Error.CommandTimeoutError,
            Error.ErrorEnable_Password,
        ) as e:
            # return เพราะ enable ไม่ได้
            print(e, ".While trying to enable device.", sep="")
            return None

        if "show vlt number" in command_dict_json:
            vlt_domain = self.get_vlt_number(command_dict_json)
            command_dict_json["show vlt status"] = f"show vlt {vlt_domain}"
            pass

        command_list = list(command_dict_json.values())
        command_list_json = list(command_dict_json.keys())

        for i in range(len(command_list_json)):
            try:
                command = command_list[i]
                result[command_list_json[i]] = self.connection.send_command(command)

            except Error.ErrorCommand as e:
                print(e)
                continue
            except Error.CommandTimeoutError as e:
                print(e)
                if self.connection.is_connection_alive():
                    # connection is alive but command doesn't return with anything skip this command
                    continue
                else:
                    # connection is loss
                    raise Error.ConnectionLossConnect(command)
            except Error.ConnectionLossConnect as e:
                # connection loss must reconnect
                print(e)
                continue

        for i in result.values():
            print(i, end=" ")
        return result

    def get_vlt_number(self, command_dict_json: dict):
        raw_vlt_num = self.connection.send_command(command_dict_json["show vlt number"])
        match = re.search(r"vlt-domain (\d+)", raw_vlt_num)
        if match:
            return int(match.group(1))
        else:
            return None
