import os
import re
import json
import ssh_module as ssh
import paramiko as para
from string import printable


class communication:
    hostname: str
    username: str
    password: str
    enable_password: str = ""
    timeout: int = 4
    banner_timeout: int = 4
    port: int = None

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

    def set_enable_password(self, enable_password: str):
        self.enable_password = enable_password

    def set_timeout(self, timeout: int):
        if timeout <= 0:
            return
        self.timeout = timeout

    def set_banner_timeout(self, banner_timeout: int):
        if banner_timeout < 0:
            return
        self.banner_timeout = banner_timeout

    def set_ssh_connection(self):
        self.connection = ssh.ssh_connection(self)
        try:
            self.connection.connect_to_device()
        except OSError as e:
            print(e)
            self.connection = None
        except para.SSHException as e:
            print(e)
            self.connection = None

    def send_list_command(self, command_list_json: dict = {}):

        if self.connection.is_enable():
            command_list_json.pop("Enable Device")
        command_list = list(command_list_json.values())
        try:
            result = ""
            for command in command_list:
                result += self.connection.send_command(command)
            print("***\n", result, "\n***")
            return result

        except Error.ErrorCommand as e:
            print(e)
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


class json_file:
    file_list: set
    os_template: dict
    command_list: list
    command_list_json: dict

    def get_list_of_file(self):
        folder_path = "./command_template"
        try:
            self.file_list = os.listdir(folder_path)

        except FileNotFoundError:
            print(f"Error: Folder '{folder_path}' not found.")
            return

    def read_json_file(self, file_name: str):
        file_path = f"./command_template/{file_name}"
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

    def get_command_json(self, OS: str):
        try:
            return self.os_template[OS]
        except (KeyError, FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error getting command list for OS {OS}: {e}")
            return None


class Error:
    class ErrorCommand(Exception):
        # Class ทำหน้าที่จัดการ Exction ของคำสั่งที่ส่งไปแล้ว อุปกรณ์ไม่เข้าใจ
        def __init__(self, command):
            self.message = f"An error occurred while executing the '{command}'"
            super().__init__(self.message)

    class ErrorEnable_Password(Exception):
        def __init__(
            self, message="An error occurred while using given enable password"
        ):
            self.message = message
            super().__init__(self.message)


if __name__ == "__main__":
    ssh_con = communication()
    file = json_file()
    file.get_list_of_file()
    file.read_json_file(file.file_list[1])

    ssh_con.set_hostname("")
    ssh_con.set_username("REDACTED")
    ssh_con.set_password("REDACTED")
    # ssh_con.set_enable_password(input("Please input enable password (enter if None): "))
    ssh_con.set_port(22)

    ssh_con.set_ssh_connection()

    print("Connect Successfuly")

    ssh_con.send_list_command(file.get_command_json("os-10"))
