class Error:
    class ErrorCommand(Exception):
        # Class ทำหน้าที่จัดการ Exction ของคำสั่งที่ส่งไปแล้ว อุปกรณ์ไม่เข้าใจ
        def __init__(self, command: str):
            self.message = f"An error occurred while executing the '{command}'"
            super().__init__(self.message)

    class ErrorEnable_Password(Exception):
        def __init__(self, wrong_password: str):
            self.message = (
                f"An error occurred while using given {wrong_password} password"
            )

            super().__init__(self.message)

    class ConnectionError(Exception):
        def __init__(self, message: str = "The Connection variable is still null"):
            self.message = message
            super().__init__(self.message)

    class CommandTimeoutError(Exception):
        def __init__(self, command: str):
            self.message = f"An error occurred while executing the '{command}', The device don't return with any thing"
            super().__init__(self.message)

    class ConnectionLossConnect(Exception):
        def __init__(self, command: str):
            self.message = f"Connection was loss while executing the '{command}'"
            super().__init__(self.message)

    class NoSerialPortError(Exception):
        def __init__(self, message: str = "Program Can't find serial port"):
            self.message = message
            super().__init__(self.message)

    class LoginError(Exception):
        def __init__(self, message: str = "Program can't do automatic login"):
            self.message = message
            super().__init__(self.message)
