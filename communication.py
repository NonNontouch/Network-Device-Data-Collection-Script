import os
import re
import json
import ssh_module as ssh
from string import printable


class communication:
    hostname: str
    username: str
    password: str
    enablepassword: str = ""
    timeout: int = 4
    banner_timeout: int = 4
    port: int = None

    connection = None

    file_list: set
    os_template: dict
    command_list: dict
    command_list_json: dict

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
        if self.port == None:
            self.port == 22
        self.connection = ssh.ssh_connection(
            hostname=self.hostname,
            username=self.username,
            password=self.password,
            enable_password=self.enablepassword,
            port=self.port,
            timeout=self.timeout,
            banner_timeout=self.banner_timeout,
        )
        self.connection.connect_to_device()

    def send_list_command(self, command_list: list = None):
        if command_list != None:
            self.connection.send_list_command(command_list)
        else:
            self.connection.send_list_command(self.command_list)
        return

    def get_file_list(self):
        folder_path = "./command_template"
        try:
            self.file_list = os.listdir(folder_path)

        except FileNotFoundError:
            print(f"Error: Folder '{folder_path}' not found.")
            return

    def get_os_template(self, filename: str):
        file_path = f"./command_template/{filename}"
        try:
            with open(file_path, "r") as f:
                self.os_template = json.load(f)
                return self.os_template
        except FileNotFoundError:
            print(f"Error: File '{file_path}' not found.")
            return None
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON in file '{file_path}'.")
            return None

    def get_command_list(self, OS: str):
        try:
            self.command_list_json = self.os_template[OS]
            self.command_list = list(self.command_list_json.values())[:-1]
            return self.command_list
        except (KeyError, FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error getting command list for OS {OS}: {e}")
            return None


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
                r"invalid|command not found|Unrecognized|Unknown command|Incomplete command|Illegal command",
                output,
                flags=re.IGNORECASE,
            )
            is not None
        )

    def remove_control_char(self, ssh_output: str):
        # ลบ control char ที่ไม่จำเป็น ให้เหลือแค่ \n\r\t
        return re.sub(r"[^\x20-\x7E\r\n\t]+", "", ssh_output)


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
    test.set_hostname("REDACTED")
    test.set_username("REDACTED")
    test.set_password("REDACTED")
    test.set_port(22)
    test.set_ssh_connection()
    test.get_file_list()
    test.get_os_template(test.file_list[1])
    test.get_command_list("os-10")
    test.send_list_command(["ter le 0", "show processes memory"])
