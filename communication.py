import os

import json
from ssh_module import ssh_connection as ssh
from telnet_module import telnet_connection as telnet
from regular_expression_handler import data_handling
from error import Error
import re as re

import paramiko as para


class connection:
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
        self.connection = ssh(self)
        try:
            self.connection.connect_to_device()
        except OSError as e:
            print(e)
            self.connection = None
        except para.SSHException as e:
            print(e)
            self.connection = None
        except Exception as e:
            print(f"Error connecting to SSH: {e}")
            self.connection = None

    def set_telnet_connection(self):
        if self.port == None:
            self.port = 23
        self.connection = telnet(self)
        try:
            self.connection.connect_to_device()
            self.connection.login()
        except Exception as e:
            print(f"Error connecting to Telnet: {e}")
            self.connection = None

    def send_list_command(self, command_list_json: dict = {}):

        if self.connection.is_enable():
            command_list_json.pop("Enable Device")
        command_list = list(command_list_json.values())
        command_list_json = list(command_list_json.keys())
        try:
            result: dict = {}
            for i in range(len(command_list_json)):
                command = command_list[i]
                result[command_list_json[i]] = data_handling.remove_control_char(
                    self.connection.send_command(command)
                )
            print("***\n", result, "\n***")
            return result

        except Error.ErrorCommand as e:
            print(e)
            return None

    def get_vlt_number(self, command_json: dict):
        self.connection.send_command("")
        raw_vlt_num = self.connection.send_command(command_json["show vlt number"])
        match = re.search(r"vlt-domain (\d+)", raw_vlt_num)
        if match:
            return int(match.group(1))
        else:
            return None


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


if __name__ == "__main__":
    # telnet_con = connection()
    # telnet_con.set_hostname("REDACTED")
    # telnet_con.set_username("REDACTED")
    # telnet_con.set_password("REDACTED")
    # telnet_con.set_telnet_connection()
    # telnet_con.set_ssh_connection()
    ssh_con = connection()
    file = json_file()
    file.get_list_of_file()
    file.read_json_file(file.file_list[1])

    ssh_con.set_hostname("REDACTED")
    ssh_con.set_username("REDACTED")
    ssh_con.set_password("REDACTED")
    # ssh_con.set_enable_password(input("Please input enable password (enter if None): "))
    ssh_con.set_port(22)

    ssh_con.set_ssh_connection()
    if ssh_con.connection == None:
        exit()
    print("Connect Successfuly")
    ssh_con.get_vlt_number(file.get_command_json("os-10"))
    ssh_con.send_list_command(file.get_command_json("os-10"))
