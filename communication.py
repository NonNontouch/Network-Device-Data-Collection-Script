import os
import re
import ssh_module as ssh
from string import printable


class communication:
    hostname = ""
    username = ""
    password = ""
    enablepassword = ""
    timeout = None
    banner_timeout = None
    port = None

    connection = None

    def set_hostname(self, hostname: str):
        self.hostname = hostname

    def set_port(self, port: int):
        if port >= 65545 or port < 1:
            return
        self.port = port

    def set_username(self, username: str):
        self.username = username

    def set_password(self, password: str):
        self.password = password

    def set_enablepassword(self, enablepassword: str):
        self.enablepassword = enablepassword

    def set_timeout(self, timeout: int):
        if timeout <= 0:
            return
        self.timeout = timeout

    def set_banner_timeout(self, banner_timeout: int):
        if banner_timeout < 0:
            return
        self.banner_timeout = banner_timeout

    def set_ssh_connection(self):
        self.connection = ssh.ssh_connection(
            hostname=self.hostname,
            username=self.username,
            password=self.password,
            enable_password=self.enablepassword,
            timeout=self.timeout,
            banner_timeout=self.banner_timeout,
        )

    def send_list_command(self):
        return

    def connect_to_ssh(self):
        self.connection.connect_to_device()
        self.connection.send_list_command(["ter le 0", "show run"])

    def get_template_name(self):
        folder_path = "./command_template"
        try:
            filenames = os.listdir(folder_path)
            print(filenames)

        except FileNotFoundError:
            print(f"Error: Folder '{folder_path}' not found.")
            return


class common_function:

    def find_prompt(self, output: str):
        if output != "":
            last_line = output.splitlines()[-1].strip()
            if re.match(r"([\w-]+)(>|(?:\(config.*\))*#)", last_line):
                return True
        return False

    def check_error(self, output: str):
        # หาคำว่า invalid หรือ command not found ถ้ามี ให้return True ถ้าไม่มี return false
        return (
            re.search(
                r"invalid|command not found|Unrecognized|Unknown command|Incomplete command",
                output,
                flags=re.IGNORECASE,
            )
            is not None
        )

    def remove_control_char(self, output: str):
        # ลบ control char ที่ไม่จำเป็น ให้เหลือแค่ \n\r\t
        keep_set = set("\n\r\t")
        return "".join(c for c in output if c.isprintable() or c in keep_set)


class Error:
    class ErrorCommand(Exception):
        # Class ทำหน้าที่จัดการ Exction ของคำสั่งที่ส่งไปแล้ว อุปกรณ์ไม่เข้าใจ
        def __init__(self, command):
            self.message = f"An error occurred while executing the '{command}'"
            super().__init__(self.message)

    class ErroeEnablePassword(Exception):
        def __init__(
            self, message="An error occurred while using given enable password"
        ):
            self.message = message
            super().__init__(self.message)


if __name__ == "__main__":
    test = communication()
    test.get_template_name()
