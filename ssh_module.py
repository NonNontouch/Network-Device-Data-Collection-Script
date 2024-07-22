import re as re
from time import sleep
import paramiko as para


class ssh_connection:
    connect = para.SSHClient()
    policy = para.AutoAddPolicy()
    session = None

    def __init__(
        self,
        hostname: str,
        username: str,
        password: str,
        port=None,
        enable_password=None,
        timeout=None,
        banner_timeout=None,
    ):
        self.hostname = hostname
        self.usename = username
        self.password = password
        if enable_password != None:
            self.enable_password = enable_password
        if port == None:
            self.port = 22
        else:
            self.port = port

        if timeout == None:
            self.timeout = 4
        else:
            self.timeout = timeout

        if banner_timeout == None:
            self.banner_timeout = 5
        else:
            self.banner_timeout = banner_timeout

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

    def find_prompt(self, output):
        last_line = output.splitlines()[-1].strip()
        if re.match(r"([\w-]+)(>|(?:\(config.*\))*#)", last_line):
            return True
        return False

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
            raise ErrorCommand(command)
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
        return self.session.recv(65535).decode("utf-8").rstrip()

    def check_error(self, output):
        # หาคำว่า invalid หรือ command not found ถ้ามี ให้return True ถ้าไม่มี return false
        return (
            re.search(r"invalid|command not found", output, flags=re.IGNORECASE)
            is not None
        )

    def get_hostname(self):
        console_name = self.send_command("")
        return

    def start_get_data(self):
        console_name = self.send_command("")
        if console_name[-1] == ">":
            try:
                if self.enable_device(self.enable_password) == False:
                    raise ErroeEnablePassword
            except TypeError as e:
                print(e)
                return
            except ErroeEnablePassword as e:
                print(e)
                return
        try:
            command_list = ["ter le 0", "show int gi 1/0/24"]
            for command in command_list:
                result = self.send_command(command=command)
            print("***\n", result, "\n***")
        except ErrorCommand as e:
            print(e)
            return

    def get_tech_support(self):
        return connection.send_command("show tech")


class ErrorCommand(Exception):
    def __init__(self, command):
        self.message = f"An error occurred while executing the '{command}'"  # Added closing quotation mark
        super().__init__(self.message)


class ErroeEnablePassword(Exception):
    def __init__(self, message="An error occurred while using given enable password"):
        self.message = message
        super().__init__(self.message)


if __name__ == "__main__":
    connection = ssh_connection(
        hostname="10.10.40.223",
        username="non",
        password="REDACTED",
        enable_password="REDACTED",
    )
    connection.connect_to_device()
    if connection.session != None:
        connection.start_get_data()
        connection.session.close()
