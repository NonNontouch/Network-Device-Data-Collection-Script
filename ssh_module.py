from re import match
from time import sleep
import paramiko as para


class ssh_connection:
    connect = para.SSHClient()
    policy = para.AutoAddPolicy()
    session = None

    def __init__(self, hostname: str, username: str, password: str, port=None):
        self.hostname = hostname
        self.usename = username
        self.password = password
        if port == None:
            self.port = 22
        else:
            self.port = port

        try:
            self.connect.set_missing_host_key_policy(self.policy)
            self.connect.connect(hostname=self.hostname, port=self.port,
                                 username=self.usename, password=self.password, banner_timeout=200)
            self.session = self.connect.invoke_shell()
        except:
            print("Error Connection ")

    def find_prompt(self, output):
        last_line = output.splitlines()[-1].strip()
        if match(r'([\w-]+)(>|(?:\(config.*\))*#)', last_line):
            return True
        return False

    def send_command(self, command):
        cmd_output = ''
        self.session.send(command + '\n')
        sleep(0.3)
        while True:
            _output = self.get_output(self.session)
            cmd_output += _output
            # print(_output)
            if self.find_prompt(_output):
                break
        return cmd_output

    def get_output(self, session):
        return session.recv(65535).decode('utf-8').rstrip()

    def start_get_data(self):
        console_name = self.send_command("\n")
        if console_name[-1] == ">":
            enable_result = self.send_command("Enable")
            for temp in ["Password", "password"]:
                if temp in enable_result:
                    self.send_command("REDACTED")
        connection.send_command("ter le 0")
        run_conf = connection.send_command("show run")
        print("***\n", run_conf, "\n***")


connection = ssh_connection("10.10.40.223", "non", "REDACTED")
connection.start_get_data()
connection.session.close()
