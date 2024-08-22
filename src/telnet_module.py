from telnetlib import Telnet
from .regular_expression_handler import data_handling
from .error import Error
from time import sleep


class telnet_connection:
    session = None

    def __init__(self, connection):
        # pass communication object into telnet_module
        self.hostname: str = connection.hostname
        self.username: str = connection.username
        self.password: str = connection.password
        self.enable_password: str = connection.enable_password
        self.port: int = connection.port
        self.timeout: int = connection.timeout
        self.banner_timeout: int = connection.banner_timeout

    def connect_to_device(self):
        try:
            self.connect = Telnet(host=self.hostname, port=self.port, timeout=4)

        except OSError as e:
            raise e
        except Exception as e:
            raise e

    def login(self):
        first_message = self.connect.read_until(b":", timeout=4).decode("utf-8")
        print(first_message, end="")
        if data_handling.is_ready_input_username(first_message):
            self.connect.write(buffer=self.to_bytes(self.username))
            sleep(0.5)
            password_prompt = self.connect.read_until(b":", timeout=4).decode("utf-8")
            print(password_prompt, end="")
            if data_handling.is_ready_input_password(password_prompt):
                self.connect.write(self.to_bytes(self.password))
                login_result = self.send_command("")
            print(login_result, end="")
        else:
            while True:
                if data_handling.is_ready_input_username(self.send_command("")):
                    break

            self.connect.write(self.username.encode("utf-8") + b"\n")

            self.connect.write(self.to_bytes(self.password))

    def send_command(self, command: str):
        cmd_output = ""
        self.connect.write(self.to_bytes(command))
        sleep(0.3)
        while True:
            _output = self.connect.read_eager().decode("utf-8")
            cmd_output += _output
            if data_handling.find_prompt(_output):
                break
        if data_handling.check_error(_output):
            raise Error.ErrorCommand(command)
        return cmd_output

    def is_enable(self):
        console_name = self.send_command("").splitlines()[-1].strip()
        return True if console_name[-1] == "#" else False

    def enable_device(self, enable_command: str, password: str):
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
            raise Error.ErrorEnable_Password(self.enable_password)

    def close_connection(self):
        # close connection and set it none
        self.connect = self.connect.close()

    @staticmethod
    def to_bytes(line):
        return f"{line}\n".encode("utf-8")
