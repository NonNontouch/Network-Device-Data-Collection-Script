from time import sleep
import paramiko as para
from communication import common_function
from communication import Error


class ssh_connection(common_function):
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
            self.banner_timeout = 10
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
        return self.remove_control_char(
            self.session.recv(65535).decode("utf-8")
        ).strip()

    def send_list_command(self, command_list):
        console_name = self.send_command("").splitlines()[-1].strip()
        if console_name[-1] == ">":
            try:
                if self.enable_device(self.enable_password) == False:
                    raise Error.ErroeEnablePassword
            except TypeError as e:
                print(e)
                return
            except Error.ErroeEnablePassword as e:
                print(e)
                return
        try:
            result = ""
            with open("myfile.txt", "w") as file:
                for command in command_list:
                    result += self.send_command(command)
                print("***\n", result, "\n***")
                # Write the string to the file
                file.write(result)
        except Error.ErrorCommand as e:
            print(e)
            return
        self.session.close()
