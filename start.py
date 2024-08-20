from src.communication import connection
from src.json_handler import json_file

if __name__ == "__main__":

    file = json_file()
    file.get_list_of_file()
    file.read_json_file(file.file_list[1])
    telnet_con = connection()
    telnet_con.set_hostname("REDACTED")
    telnet_con.set_username("REDACTED")
    telnet_con.set_password("REDACTED")
    # telnet_con.set_enable_password("REDACTED")
    # telnet_con.set_port(5000)
    telnet_con.set_telnet_connection()
    telnet_con.send_list_command(file.get_command_json("os-10"))
    # print(telnet_con.connection.send_command("enable"))
    # print(telnet_con.connection.send_command("ter len 0"))
    # print(telnet_con.connection.send_command("show run"))

    # อ่านข้อมูลจนปิด connection และเก็บในตัวแปร output


"""ssh_con = connection()
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
ssh_con.send_list_command(file.get_command_json("os-10"))"""
