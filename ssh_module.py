from time import sleep
import paramiko as para
from communication import communication
from communication import common_function
from communication import Error


class ssh_connection(
    common_function,
):
    connect = para.SSHClient()
    policy = para.AutoAddPolicy()
    session = None

    def __init__(self, communication: communication):
        # pass communication object into ssh_module
        self.hostname = communication.hostname
        self.usename = communication.username
        self.password = communication.password
        self.enable_password = communication.enable_password
        self.port = communication.port
        self.timeout = communication.timeout
        self.banner_timeout = communication.banner_timeout

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
        except OSError as e:
            print(e)
            return e
        except para.SSHException as e:
            print(e)
            return e

    def send_command(self, command):
        cmd_output = ""
        self.session.send(command + "\n")
        sleep(0.3)
        while True:
            _output = self.get_output()
            cmd_output += _output
            if self.find_prompt(_output):
                break
        if self.check_error(_output):
            raise Error.ErrorCommand(command)

        return cmd_output

    def enable_device(self, password: str):
        self.session.send("enable" + "\n")
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
                return False
        return True

    def get_output(self):
        return self.remove_control_char(self.session.recv(65535).decode("utf-8"))

    def send_list_command(self, command_list: list):
        console_name = self.send_command("").splitlines()[-1].strip()
        if console_name[-1] == ">":
            try:
                if self.enable_device(self.enable_password) == False:
                    raise Error.ErrorEnable_Password
            except TypeError as e:
                print(e)
                return
            except Error.ErrorEnable_Password as e:
                print(e)
                return
        try:
            result = ""
            for command in command_list:
                result += self.send_command(command)
            print("***\n", result, "\n***")
            return result

        except Error.ErrorCommand as e:
            print(e)
            return 
