from telnetlib import Telnet
from .regular_expression_handler import data_handling
import src.error as Error
from time import sleep


class telnet_connection:
    """_This is class responsible for Telnet Communication which use telnetlib library._\n
    _To use this class you must init and then use connect to device funciton._"""

    session = None

    def __init__(self, connection):
        """_init the serial connection module with connection variable._

        Args:
            connection (_class connection_): _A connection class with ready to use variable._
        """
        # pass communication object into telnet_module
        self._hostname: str = connection.hostname
        self._username: str = connection.username
        self._password: str = connection.password
        self._enable_password: str = connection.enable_password
        self._port: int = connection.port
        self._timeout: float = connection.timeout
        self._login_wait_time: float = connection.login_wait_time
        self._banner_timeout: float = connection.banner_timeout
        self._RETRY_DELAY: float = connection.command_retriesdelay
        self._MAX_RETRIES: int = connection.command_maxretries

    def connect_to_device(self):
        """_This function will try connect into device via Telnet._

        Raises:
            e: _description_
            e: _description_
        """
        try:
            self.connect = Telnet(host=self._hostname, port=self._port, timeout=4)

        except OSError as e:
            raise e
        except Exception as e:
            raise e

    def is_login(self):
        """_Check if device is already logged in._

        Returns:
            bool: _True if logged in, False if not._
        """
        # self.connect.write(b"\n")
        sleep(self._login_wait_time)
        try:
            console_name = (
                self.connect.read_eager().decode("utf-8").splitlines()[-1].strip()
            )
            return True if data_handling.find_prompt(console_name) else False
        except Exception:
            raise Error.LoginError("Program can't find the username form in login form")

    def login(self):
        try:
            if self.is_login():
                return
            self.connect.write(b"\n")
            first_message = self.connect.read_until(
                b":", timeout=self._login_wait_time
            ).decode("utf-8")
            print(first_message, end="")
            if data_handling.is_ready_input_username(first_message):
                sleep(self._login_wait_time)
                self.connect.write(buffer=self.to_bytes(self._username))
                sleep(self._login_wait_time)
                password_prompt = self.connect.read_until(
                    b":", timeout=self._login_wait_time
                ).decode("utf-8")
                print(password_prompt, end="")
                if self._username not in password_prompt:
                    raise Error.LoginError(
                        "Program couldn't send data via Telnet, Could be blocked by firewall"
                    )
                if data_handling.is_ready_input_password(password_prompt):
                    sleep(self._login_wait_time)
                    self.connect.write(self.to_bytes(self._password))
                    count = 0
                    while True:
                        sleep(0.5)
                        login_result = self.connect.read_eager().decode("utf-8")
                        if data_handling.find_prompt(login_result):
                            break
                        if count >= self._banner_timeout:
                            raise Error.LoginError("Username or Password is wrong.")
                        count += 0.5

                    print(login_result, end="")
            else:
                raise Error.LoginError()
        except (EOFError, OSError):
            # If connection is closed while reading or writing
            raise Error.ConnectionLossConnect("Login")

    def send_command(
        self,
        command: str,
    ):
        """_Send command to a host via Telnet._

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
        except OSError as e:
            print(e)
            raise Error.ConnectionLossConnect(command)

        sleep(0.3)

        while True:
            try:
                _output = data_handling.remove_control_char(self.get_output())
            except EOFError as e:
                print(e)
                raise Error.ConnectionLossConnect(command)

            if not _output:  # Check for empty output
                retries += 1
                if retries > self._MAX_RETRIES:
                    raise Error.CommandTimeoutError(command)
                sleep(self._RETRY_DELAY)  # Use the command timeout here
                continue  # Continue to the next iteration

            # Handle "More" prompt
            if "More" in _output or "more" in _output:
                self.connect.write(b" ")
                _output = data_handling.remove_more_keyword(_output)

            cmd_output += _output
            retries = 0  # Reset retries on valid output

            # Check for prompt to break the loop
            if data_handling.find_prompt(_output):
                break

        if data_handling.check_error(cmd_output):
            raise Error.ErrorCommand(command, cmd_output)

        return cmd_output

    def get_output(self):
        return self.connect.read_eager().decode("utf-8")

    def is_enable(self):
        """_Check if device is enable._

        Returns:
            bool: _True if enabled, False if not._
        """
        console_name = self.send_command("").splitlines()[-1].strip()
        return True if console_name[-1] == "#" else False

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

        _output = self.connect.read_eager().decode("utf-8")
        if _output[-1] == "#":
            return
        for text in ["Password:", "password:"]:
            if text in _output:
                _output = self.send_command(password)
                break
        if _output[-1] == "#":
            return
        else:
            raise Error.ErrorEnable_Password(password)

    def close_connection(self):
        """_Close connection and set connect variable to None._"""
        # close connection and set it none
        self.connect = self.connect.close()

    def is_connection_alive(self):
        try:
            # Send a null byte (or a newline) to check if the connection is alive
            self.connect.write(b"\n")
            self.connect.read_until(b"\n", timeout=self._RETRY_DELAY)
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
