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

    def set_parameters(self, params: dict):
        """Set multiple connection parameters from a dictionary.

        Args:
            params (dict): A dictionary containing connection parameters.
        """
        if "hostname" in params and params["hostname"].strip():
            self.set_hostname(params["hostname"])
        if "port" in params and params["port"].strip():
            self.set_port(int(params["port"]))  # Convert to int if valid
        if "username" in params and params["username"].strip():
            self.set_username(params["username"])
        if "password" in params and params["password"].strip():
            self.set_password(params["password"])
        if "enable_password" in params and params["enable_password"].strip():
            self.set_enable_password(params["enable_password"])
        if "timeout" in params and params["timeout"].strip():
            self.set_timeout(float(params["timeout"]))  # Convert to float if valid
        if "login_wait_time" in params and params["login_wait_time"].strip():
            self.set_login_wait_time(float(params["login_wait_time"]))
        if "command_retriesdelay" in params and params["command_retriesdelay"].strip():
            self.set_command_retries_delay(float(params["command_retriesdelay"]))
        if "banner_timeout" in params and params["banner_timeout"].strip():
            self.set_banner_timeout(int(params["banner_timeout"]))
        if "command_maxretries" in params and params["command_maxretries"].strip():
            self.set_command_maxretries(int(params["command_maxretries"]))
        if "baudrate" in params and params["baudrate"].strip():
            self.set_baudrate(int(params["baudrate"]))
        if "bytesize" in params and params["bytesize"].strip():
            self.set_bytesize(int(params["bytesize"]))
        if "parity" in params and params["parity"].strip():
            self.set_parity(params["parity"])
        if "stopbits" in params and params["stopbits"].strip():
            self.set_stopbits(float(params["stopbits"]))

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
        if parity in serial.get_parity_type():
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
        except (OSError, para.SSHException) as e:
            print(e)
            self.connection = None
            raise e  # Re-raise the exception for further handling
        except Exception as e:
            print(f"Error connecting to SSH: {e}")
            self.connection = None
            raise e

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
            raise e

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
            raise e

    def get_serial_port(self):
        """_Get list of all avaiable serial port in computer._"""
        if isinstance(self.connection, serial):
            self.serial_port_list = self.connection.list_serial_ports()
            return self.serial_port_list

    def send_list_command(self, command_dict_json: dict):
        """
        Send command to device from the sequence given in the dict argument.

        Args:
            command_dict_json (dict): A dict variable containing command templates.

        Raises:
            Error.ConnectionError: If connection is None, this function will raise this error.

        Returns:
            dict: A dict of command results from the given commands.
        """
        # Create a copy of the command dictionary to avoid modifying the original
        temp_command_dict_json = command_dict_json.copy()
        result = {}

        # Check connection status
        if self.connection is None:
            raise Error.ConnectionError("No connection established.")

        # Attempt to enable the device if necessary
        self._enable_device_if_needed(temp_command_dict_json)

        # Check for VLT number command and update command list if present
        self._update_vlt_status(temp_command_dict_json)

        # Prepare the command list
        command_list_json = list(temp_command_dict_json.keys())
        command_list = list(temp_command_dict_json.values())

        # Send commands to the device
        for command_key, command in zip(command_list_json, command_list):
            result[command_key] = self._send_command(command_key, command)

        # Log results and close connection
        self.connection.close_connection()
        for output in result.values():
            print(output, end=" ")

        return result

    def _enable_device_if_needed(self, command_dict):
        """Enable the device if it's not already enabled."""
        try:
            if not self.connection.is_enable():
                enable_command = command_dict.pop("Enable Device", None)
                if enable_command:
                    self.connection.enable_device(enable_command, self.enable_password)
                else:
                    raise Error.LoginError("Program can't enable device")
        except (
            Error.ErrorCommand,
            Error.ConnectionLossConnect,
            Error.CommandTimeoutError,
            Error.ErrorEnable_Password,
        ) as e:
            print(e, ".While trying to enable device.", sep="")
            raise Error.LoginError("Program can't enable device")

    def _update_vlt_status(self, command_dict):
        """Update the VLT status in the command dictionary if 'show vlt number' is present."""
        if "show vlt number" in command_dict:
            try:
                vlt_domain = self.get_vlt_number(command_dict)
                command_dict["show vlt status"] = f"show vlt {vlt_domain}"
            except Exception:
                raise Error.ErrorGetVLTNumber()

    def _send_command(self, command_key, command):
        """Send a single command and handle errors."""
        try:
            return self.connection.send_command(command)
        except Error.ErrorCommand as e:
            print(e)
            return str(e)
        except Error.CommandTimeoutError as e:
            print(e)
            if self.connection.is_connection_alive():
                return str(e)  # Skip this command if connection is alive
            else:
                raise Error.ConnectionLossConnect(command)
        except Error.ConnectionLossConnect as e:
            raise Error.ConnectionLossConnect(command)

    def get_vlt_number(self, command_dict_json: dict):
        raw_vlt_num = self.connection.send_command(command_dict_json["show vlt number"])
        match = re.search(r"vlt-domain (\d+)", raw_vlt_num)
        if match:
            return int(match.group(1))
        else:
            return None
