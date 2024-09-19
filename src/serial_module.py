from .regular_expression_handler import data_handling
import src.error as Error
from time import sleep
from serial import Serial
from serial import serialutil
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
        self._username: str = connection.username
        self._password: str = connection.password
        self._enable_password: str = connection.enable_password
        self._timeout: float = connection.timeout
        self._banner_timeout: float = connection.banner_timeout
        self._RETRY_DELAY: float = connection.command_retriesdelay
        self._MAX_RETRIES: int = connection.command_maxretries
        self._baudrate: int = connection.baudrate
        self._bytesize: int = connection.bytesize
        self._parity: str = connection.parity
        self._stopbits: float = connection.stopbits

    def set_serial_object(self):
        """_This function will create Serial Module with given varialbe._

        Raises:
            e: _All Excetion will be raise by this variable._
        """
        try:
            self.connect = Serial(
                timeout=self._timeout,
                baudrate=self._baudrate,
                bytesize=self._bytesize,
                parity=self._parity,
                stopbits=self._stopbits,
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

        try:
            self.connect.write(self.to_bytes(command))
        except serialutil.SerialTimeoutException:
            raise Error.ConnectionLossConnect(command)

        sleep(0.3)

        while True:
            try:
                _output = data_handling.remove_control_char(self.get_output())
            except OSError:
                raise Error.ConnectionLossConnect(command)

            if not _output:  # Check for empty output
                retries += 1
                if retries > self._MAX_RETRIES:
                    raise Error.CommandTimeoutError(command)
                sleep(self._RETRY_DELAY)  # Use command timeout for waiting
                continue  # Continue to the next iteration

            # Handle "More" prompt
            if "More" in _output or "more" in _output:
                self.connect.write(" ")
                _output = data_handling.remove_more_keyword(_output)

            cmd_output += _output
            retries = 0  # Reset retries on valid output

            # Check for prompt to break the loop
            if data_handling.find_prompt(_output):
                break

        if data_handling.check_error(cmd_output):
            raise Error.ErrorCommand(command, cmd_output)

        return cmd_output

    def login(self):
        """_This function will try login into device via Serial._

        Raises:
            Error.LoginError: _If login goes wrong. Such as the response doesn't seems normal._
        """

        try:
            if self.is_login():
                return
            self.connect.write(self.to_bytes(""))
            first_message = self.connect.read_until(b":").decode("utf-8")
            print(first_message, end="")
            if data_handling.is_ready_input_username(first_message):
                self.connect.write(self.to_bytes(self._username))
                sleep(0.5)
                password_prompt = self.connect.read_until(b":").decode("utf-8")
                print(password_prompt, end="")
                if data_handling.is_ready_input_password(password_prompt):
                    self.connect.write(self.to_bytes(self._password))
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

                self.connect.write(self._username.encode("utf-8") + b"\n")
                self.connect.write(self.to_bytes(self._password))
        except (serialutil.SerialTimeoutException, OSError):
            raise Error.ConnectionLossConnect("Login")
        except IndexError:
            raise Error.LoginError("Program can't check if is login")

    def get_output(self):
        """_This funciton will read all data in serial port._

        Returns:
            str: _A string of data in serial port which decoded by utf-8._
        """
        return self.connect.read_all().decode("utf-8")

    def enable_device(self, enable_command: str, password: str):
        """_This function will make device in Privileged EXEC mode. _

        Args:
            enable_command (str): _description_
            password (str): _description_

        Raises:
            Error.ErrorEnable_Password: _description_
        """
        self.connect.write(self.to_bytes(enable_command))
        sleep(0.3)

        _output = self.connect.read_until(b":").decode("utf-8")
        for text in ["Password:", "password:"]:
            if text in _output:
                _output = self.send_command(password)
                break
        if _output[-1] == "#":
            return
        else:
            raise Error.ErrorEnable_Password(self._enable_password)

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
        self.connect.write(b"\n")
        console_name = self.connect.read_all().decode("utf-8").splitlines()[-1].strip()
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

    def is_connection_alive(self):
        try:
            # Send a null byte (or a newline) to check if the connection is alive
            self.connect.write(b"\n")
            self.connect.read_until(b"\n")
            return True
        except (EOFError, ConnectionResetError, ConnectionAbortedError, OSError):
            # If any of these exceptions are raised, the connection is not alive
            return False

    @staticmethod
    def to_bytes(line: str):
        """return a bytes of string which also include \\n

        Args:
            line (_str_): a string that will convert to byte

        Returns:
            byte: byte string with \\n in the end
        """
        return f"{line}\n".encode("utf-8")
