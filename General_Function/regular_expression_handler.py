import re


class data_handling:

    def find_prompt(output: str):
        if output != "":
            last_line = output.splitlines()[-1].strip()
            if re.match(r"([\w-]+)(>|(?:\(config.*\))*#)", last_line):
                return True
        return False

    def check_error(output: str):
        # หาคำว่า invalid หรือ command not found ถ้ามี ให้return True ถ้าไม่มี return false
        return (
            re.search(
                r"invalid|command not found|Unrecognized|Unknown command|Incomplete command|Illegal command",
                output,
                flags=re.IGNORECASE,
            )
            is not None
        )

    def remove_control_char(ssh_output: str):
        # ลบ control char ที่ไม่จำเป็น ให้เหลือแค่ \n\r\t
        return re.sub(r"[^\x20-\x7E\r\n\t]+", "", ssh_output)

    def is_ready_input_username(telnet_output: str):
        return (
            re.search(
                r"(?:login|username|user)(?!.*password:pass|Password)",
                telnet_output,
                flags=re.IGNORECASE,
            )
            is not None
        )

    def is_ready_input_password(telnet_output: str):
        return (
            re.search(
                r"(?:password:pass|Password)(?!.*login|username|user)",
                telnet_output,
                flags=re.IGNORECASE,
            )
            is not None
        )
