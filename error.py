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
