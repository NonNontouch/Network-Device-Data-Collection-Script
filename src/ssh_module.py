import socket
from time import sleep
import paramiko as para
from .regular_expression_handler import data_handling
from .error import Error


class ssh_connection:
    connect = para.SSHClient()
    policy = para.AutoAddPolicy()
    session = None

    def __init__(self, communication):
        # pass communication object into ssh_module
        self.hostname = communication.hostname
        self.usename = communication.username
        self.password = communication.password
        self.enable_password = communication.enable_password
        self.port = communication.port
        self.timeout = communication.timeout
        self.banner_timeout = communication.banner_timeout
        self.command_timeout = communication.command_timeout

    def connect_to_device(self):
        try:
            self.connect.set_missing_host_key_policy(self.policy)
            self.connect.connect(
                hostname=self.hostname,
                port=self.port,
                username=self.usename,
                password=self.password,
                timeout=self.timeout,
                banner_timeout=self.banner_timeout,
            )
            self.session = self.connect.invoke_shell()
            self.session.settimeout(self.command_timeout)

        except OSError as e:
            raise e
        except para.SSHException as e:
            raise e
        except Exception as e:
            raise e

    def send_command(
        self, command: str, max_retries: int = 4, command_timeout: int = 1
    ):
        if self.is_connection_alive():
            self.session.settimeout(command_timeout)
            retries = 0
            cmd_output = ""
            try:
                self.session.send(command + "\n")
            except socket.timeout:
                raise Error.ConnectionLossConnect(command)
            except socket.error:
                raise Error.ConnectionLossConnect(command)
            sleep(0.3)
            while True:
                _output = self.get_output()
                if _output == "":
                    retries += 1
                    if retries > max_retries:
                        raise Error.CommandTimeoutError(command)
                    sleep(1)
                elif "More" in _output or "more" in _output:
                    self.session.send(" ")
                    _output = data_handling.remove_more_keyword(_output)
                    cmd_output += _output
                else:
                    cmd_output += _output
                    if data_handling.find_prompt(_output):
                        break
            if data_handling.check_error(_output):
                raise Error.ErrorCommand(command)
            return cmd_output
        else:
            raise Error.ConnectionLossConnect(command)

    def enable_device(self, enable_command: str, password: str):
        if self.is_enable() == True:
            # device already enable
            return
        self.session.send(f"{enable_command}" + "\n")
        sleep(0.3)
        while True:
            _output = self.get_output()
            for text in ["Password:", "password:"]:
                if text in _output:
                    _output = self.send_command(password)
                    break
            if _output[-1] == "#":
                break
            else:
                raise Error.ErrorEnable_Password(password)
        return

    def is_enable(self):
        console_name = self.send_command("").splitlines()[-1].strip()
        return True if console_name[-1] == "#" else False

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
