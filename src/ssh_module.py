import socket
from time import sleep
import paramiko as para
from .regular_expression_handler import data_handling
import src.error as Error


class ssh_connection:
    """_Class that handle ssh connection._


    Raises:
        OSError: _When connection to host is loss or unable to conenct._
        para.SSHException: _When can't access host ssh server._
        Exception: _Any exceltion._
        Error.ConnectionLossConnect: _When Connection is loss while send and receive data._
        Error.CommandTimeoutError: _When sended command return with nothing for period of time._
        Error.ErrorCommand: _When sened command return with error keywords._
        Error.ErrorEnable_Password: _When given enable is wrong._

    Returns:
        _type_: _description_
    """

    connect = para.SSHClient()
    policy = para.AutoAddPolicy()
    session = None

    def __init__(self, connection, data_handling: data_handling = None):
        # pass connection object into ssh_module
        self._hostname: str = connection.hostname
        self._username: str = connection.username
        self._password: str = connection.password
        self._port: int = connection.port
        self._timeout: float = connection.timeout
        self._banner_timeout: float = connection.banner_timeout
        self._RETRY_DELAY: float = connection.command_retriesdelay
        self._MAX_RETRIES: int = connection.command_maxretries
        self._data_handling = data_handling

    def connect_to_device(self, command_regex):
        try:
            self.connect.set_missing_host_key_policy(self.policy)
            self.connect.connect(
                hostname=self._hostname,
                port=self._port,
                username=self._username,
                password=self._password,
                timeout=self._timeout,
                banner_timeout=self._banner_timeout,
            )
            self.session = self.connect.invoke_shell()
            self.session.settimeout(self._RETRY_DELAY)
            self.find_prompt_regex = command_regex["find_prompt"]
            self.enable_ending = command_regex["enable_ending"]
        except OSError as e:
            raise OSError(e)
        except para.SSHException as e:
            raise para.SSHException(e)
        except Exception as e:
            raise Exception(e)

    def send_command(self, command: str):
        if not self.is_connection_alive():
            raise Error.ConnectionLossConnect(command)

        retries = 0

        cmd_output = ""

        try:
            self.session.send(command + "\n")
        except socket.timeout:
            raise Error.ConnectionLossConnect(command)

        sleep(0.3)

        while True:
            _output = self._data_handling.remove_control_char(self.get_output())

            if not _output:  # Check for empty output
                retries += 1
                if retries > self._MAX_RETRIES:
                    raise Error.CommandTimeoutError(command)
                sleep(self._RETRY_DELAY)
                continue

            # Handle "More" prompt
            if "More" in _output or "more" in _output:
                self.session.send(" ")
                _output = self._data_handling.remove_more_keyword(_output)

            # Append output to cmd_output
            cmd_output += _output
            retries = 0  # Reset retries on valid output

            # Check for prompt to break the loop
            if self._data_handling.find_prompt(_output, self.find_prompt_regex):
                break

        # Check for errors in the command output
        if self._data_handling.check_error(cmd_output):
            raise Error.ErrorCommand(command, cmd_output)

        return cmd_output

    def enable_device(self, enable_command: str, password: str):
        self.session.send(f"{enable_command}" + "\n")
        sleep(0.3)

        _output = self.get_output()
        if self._data_handling.is_ready_input_password(_output):
            _output = self.send_command(password)
        if _output[-1] == self.enable_ending:
            return
        else:
            raise Error.ErrorEnable_Password(password)

    def is_enable(self):
        console_name = self.send_command("").splitlines()[-1].strip()
        return True if console_name[-1] == self.enable_ending else False

    def get_output(self):
        try:
            return self.session.recv(65535).decode("utf-8")
        except socket.timeout:
            return ""

    def is_connection_alive(self):
        return (
            True
            if self.connect.get_transport() is not None
            and self.connect.get_transport().is_active()
            else False
        )

    def close_connection(self):
        self.session.close()
        self.connect = None
