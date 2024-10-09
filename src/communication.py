from .ssh_module import ssh_connection as ssh
from .telnet_module import telnet_connection as telnet
from .serial_module import serial_connection as serial
import src.error as Error
from .regular_expression_handler import data_handling
from .config_handler import ConfigHandler
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
    regex: str = r"^\s*([\w-]+)(>|#)\s*$"
    connection = None

    def __init__(self):
        # Load configuration when initializing the class
        self.config = ConfigHandler("config.json")
        self.config.load_config()

        self.data_handling = data_handling("config.json")

        # Load other configurable values
        self.timeout: float = (
            self.config.get("timeout", self.timeout) if self.config else self.timeout
        )
        self.login_wait_time: float = (
            self.config.get("login_wait_time", self.login_wait_time)
            if self.config
            else self.login_wait_time
        )
        self.banner_timeout: float = (
            self.config.get("banner_timeout", self.banner_timeout)
            if self.config
            else self.banner_timeout
        )
        self.command_retriesdelay: float = (
            self.config.get("command_retriesdelay", self.command_retriesdelay)
            if self.config
            else self.command_retriesdelay
        )
        self.command_maxretries: int = (
            self.config.get("command_maxretries", self.command_maxretries)
            if self.config
            else self.command_maxretries
        )
        self.port: int = (
            self.config.get("port", self.port) if self.config else self.port
        )
        self.baudrate: int = (
            self.config.get("baudrate", self.baudrate) if self.config else self.baudrate
        )
        self.bytesize: int = (
            self.config.get("bytesize", self.bytesize) if self.config else self.bytesize
        )
        self.parity: str = (
            self.config.get("parity", self.parity) if self.config else self.parity
        )
        self.stopbits: float = (
            self.config.get("stopbits", self.stopbits) if self.config else self.stopbits
        )

    def set_parameters(self, params: dict):
        """Set multiple connection parameters from a dictionary."""
        for key, value in params.items():
            if hasattr(self, key) and value is not None and str(value).strip():
                # Convert types where necessary
                if key in [
                    "timeout",
                    "login_wait_time",
                    "banner_timeout",
                    "command_retriesdelay",
                    "command_maxretries",
                    "baudrate",
                    "bytesize",
                    "stopbits",
                ]:
                    setattr(self, key, float(value))
                elif key in ["port"]:
                    setattr(self, key, int(value))
                else:
                    setattr(self, key, value)
        self.save_config("config.json")

    def get_curr_conf(self):
        """Get all connection parameters as a dictionary.
        Returns:
            dict: A dictionary containing all connection parameters.
        """
        return {
            "hostname": self.hostname,
            "port": self.port,
            "username": self.username,
            "password": self.password,
            "enable_password": self.enable_password,
            "timeout": self.timeout,
            "login_wait_time": self.login_wait_time,
            "command_retriesdelay": self.command_retriesdelay,
            "banner_timeout": self.banner_timeout,
            "command_maxretries": self.command_maxretries,
            "baudrate": self.baudrate,
            "bytesize": self.bytesize,
            "parity": self.parity,
            "stopbits": self.stopbits,
        }

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
        self.connection = ssh(self, self.data_handling)
        try:
            self.connection.connect_to_device(self.regex)
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
        self.connection = telnet(self, self.data_handling)
        try:
            self.connection.connect_to_device(self.regex)
            self.connection.login()
        except Exception as e:
            print(f"Error connecting to Telnet: {e}")
            self.connection = None
            raise e

    def set_serial_connection(self):
        """
        Set connection as serial and try connect and login to it
        """
        self.connection = serial(self, self.data_handling)
        try:
            self.connection.set_serial_object(self.regex)
            print(self.serial_port, self.baudrate)
            self.connection.connect_to_device(self.serial_port)
            self.connection.login()
        except Exception as e:
            print(f"Error connecting to Serial: {e}")
            self.connection = None
            raise e

    def get_serial_port(self):
        """_Get list of all avaiable serial port in computer._"""
        temp_serial_obj = serial(self)
        self.serial_port_list = temp_serial_obj.list_serial_ports()
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
        temp_command_dict = {}
        for command_name, command_info in temp_command_dict_json.items():
            # Access the command and active status
            if command_info["active"] == True:
                temp_command_dict[command_name] = command_info["command"]
        result = {}

        # Check connection status
        if self.connection is None:
            raise Error.ConnectionError("No connection established.")

        # Attempt to enable the device if necessary
        self._enable_device_if_needed(temp_command_dict, self.regex)

        # Check for VLT number command and update command list if present
        self._update_vlt_status(temp_command_dict)

        # Prepare the command list
        command_list_json = list(temp_command_dict.keys())
        command_list = list(temp_command_dict.values())

        # Send commands to the device
        for command_key, command in zip(command_list_json, command_list):
            print("Sending", command)
            result[command_key] = self._send_command(command_key, command)
            print("Sending", command, "Done")
        # Log results and close connection
        self.connection.close_connection()

        return result

    def _enable_device_if_needed(self, command_dict: dict, regex: str):
        """Enable the device if it's not already enabled."""
        try:
            if self.connection.is_enable() is False:
                if "Enable Device" in command_dict:
                    self.connection.enable_device(
                        enable_command=command_dict["Enable Device"],
                        password=self.enable_password,
                    )
                    print("Enable Done")
                else:
                    raise Error.LoginError("Program can't enable device")
            if "Enable Device" in command_dict:
                command_dict.pop("Enable Device")
        except (
            Error.ErrorCommand,
            Error.ConnectionLossConnect,
            Error.CommandTimeoutError,
            Error.ErrorEnable_Password,
            Exception,
        ) as e:
            print(e, ".While trying to enable device.", sep="")
            raise Error.LoginError("Program can't enable device")

    def _update_vlt_status(self, command_dict):
        """Update the VLT status in the command dictionary if 'show vlt number' is present."""
        if "show vlt number" in command_dict:
            try:
                vlt_domain = self.get_vlt_number(command_dict)
                print("Vlt domain:", vlt_domain)
                if vlt_domain is None:
                    print("command is poped")
                    command_dict.pop("show vlt status")

                command_dict["show vlt status"] = f"show vlt {vlt_domain}"
            except Exception as e:
                print(e)
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
        raw_vlt_num = self._send_command(
            command_key=["show vlt number"],
            command=command_dict_json["show vlt number"],
        )
        match = re.search(r"vlt-domain (\d+)", raw_vlt_num)
        if match:
            return int(match.group(1))
        else:
            return None

    def save_config(self, file_path: str):
        """Save the current connection parameters to a JSON file, merging with existing settings."""

        # Prepare new configuration
        new_config = {
            "timeout": self.timeout,
            "login_wait_time": self.login_wait_time,
            "banner_timeout": self.banner_timeout,
            "command_retriesdelay": self.command_retriesdelay,
            "command_maxretries": self.command_maxretries,
            "baudrate": self.baudrate,
            "bytesize": self.bytesize,
            "parity": self.parity,
            "stopbits": self.stopbits,
        }
        self.config.save_config(new_config)

        # Update existing config with new config values
