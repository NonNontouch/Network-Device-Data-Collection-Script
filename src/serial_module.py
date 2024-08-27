from .regular_expression_handler import data_handling
from .error import Error
from time import sleep
from serial import Serial
import serial.tools.list_ports


class serial_connection:
    """_This is class responsible for Serial Communication which use pyserial library._\n
    _To use this class you must init and then use connect to device funciton._"""

    port: str

    def __init__(self, connection):
        """_init the serial connection module with connection variable._

        Args:
            connection (_class connection_): _A connection class with ready to use variable._
        """
        self.username: str = connection.username
        self.password: str = connection.password
        self.enable_password: str = connection.enable_password
        self.timeout: float = connection.timeout
        self.banner_timeout: float = connection.banner_timeout
        self.command_timeout: float = connection.command_timeout
        self.baudrate: int = connection.baudrate
        self.bytesize: int = connection.bytesize
        self.parity: str = connection.parity
        self.stopbits: float = connection.stopbits

    def set_serial_object(self):
        """_This function will create Serial Module with given varialbe._

        Raises:
            e: _All Excetion will be raise by this variable._
        """
        try:
            self.connect = Serial(
                timeout=self.timeout,
                baudrate=self.baudrate,
                bytesize=self.bytesize,
                parity=self.parity,
                stopbits=self.stopbits,
            )
        except Exception as e:
            raise e

    def connect_to_device(self, serial_port):
        try:
            self.connect.port = serial_port

            self.connect.open()
        except Exception:
            print("port can't be open")
            self.connect.port = None
            raise Error.SerialConnectError(serial_port)

    def send_command(
        self,
        command: str,
        command_timeout: float = 0,
        max_retries: int = 4,
    ):
        """_Send command to a host via Serial._

        Args:
            command (_str_): _A command you want to send to this host._

        Raises:
            Error.ErrorCommand: _When command given has return with error in command result string._

        Returns:
            string: _A result from given command._
        """
        retries = 0
        cmd_output = ""
        if command_timeout == 0:
            command_timeout == self.command_timeout
        self.connect.write(self.to_bytes(command))
        sleep(0.3)
        while True:
            _output = self.get_output()
            if _output == "":
                retries += 1
                if retries > max_retries:
                    raise Error.CommandTimeoutError(command)

                sleep(command_timeout)
            elif "More" in _output or "more" in _output:
                self.connect.write(" ")
                _output = data_handling.remove_more_keyword(_output)
                cmd_output += _output
            else:
                cmd_output += _output
                if data_handling.find_prompt(_output):
                    break
        if data_handling.check_error(cmd_output):
            # Command is successfully ran but need to check for error
            raise Error.ErrorCommand(command, cmd_output)
        return cmd_output

    def login(self):
        """_This function will try login into device via Serial._

        Raises:
            Error.LoginError: _If login goes wrong. Such as the response doesn't seems normal._
        """
        if self.is_login():
            return
        self.connect.write(self.to_bytes(""))
        first_message = self.connect.read_until(b":").decode("utf-8")
        print(first_message, end="")
        if data_handling.is_ready_input_username(first_message):
            self.connect.write(self.to_bytes(self.username))
            sleep(0.5)
            password_prompt = self.connect.read_until(b":").decode("utf-8")
            print(password_prompt, end="")
            if data_handling.is_ready_input_password(password_prompt):
                self.connect.write(self.to_bytes(self.password))
                login_result = self.send_command("")
            print(login_result, end="")
            print()
        else:
            count = 0
            while True:
                self.connect.write(self.to_bytes(""))
                return_prompt = self.connect.read_until(
                    b":",
                ).decode("utf-8")
                if data_handling.is_ready_input_username(return_prompt):
                    break
                count += 1
                if count == 5:
                    raise Error.LoginError()

            self.connect.write(self.username.encode("utf-8") + b"\n")
            self.connect.write(self.to_bytes(self.password))

    def get_output(self):
        """_This funciton will read all data in serial port._

        Returns:
            str: _A string of data in serial port which decoded by utf-8._
        """
        return self.connect.read_all().decode("utf-8")

    def is_enable(self):
        """_Check if device is enable._

        Returns:
            bool: _True if enabled, False if not._
        """
        console_name = self.send_command("").splitlines()[-1].strip()
        return True if console_name[-1] == "#" else False

    def is_login(self):
        """_Check if device is already logged in._

        Returns:
            bool: _True if logged in, False if not._
        """
        console_name = self.send_command("").splitlines()[-1].strip()
        return True if data_handling.find_prompt(console_name) else False

    def list_serial_ports(self):
        """
        _Lists the names of available serial ports on the system._

        Raises:
            Error.NoSerialPortError: _A list of strings representing the names of available serial ports.If no ports are found, an empty list is returned._

        Returns:
            list: _A list of avaialbe serial port._
        """
        ports = serial.tools.list_ports.comports()

        if ports:
            available_ports = [port.device for port in ports]
            return available_ports
        else:
            raise Error.NoSerialPortError

    @staticmethod
    def to_bytes(line: str):
        """return a bytes of string which also include \\n

        Args:
            line (_str_): a string that will convert to byte

        Returns:
            byte: byte string with \\n in the end
        """
        return f"{line}\n".encode("utf-8")
