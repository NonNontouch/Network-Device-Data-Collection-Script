class ErrorCommand(Exception):
    """_Error Class that handle when command given to device is returned error._"""

    def __init__(self, command: str, command_output: str):
        """_init the class._

        Args:
            command (str): _Command that is used._
            command_output (str): _Output of given command._
        """
        self.message = f"An error occurred while executing the '{command}', \nIt gives output '{command_output}'"
        super().__init__(self.message)


class ErrorEnable_Password(Exception):
    def __init__(self, wrong_password: str):
        self.message = f"An error occurred while using given {wrong_password} password"

        super().__init__(self.message)


class ConnectionError(Exception):
    def __init__(self, message: str = "The Connection variable is still null"):
        self.message = message
        super().__init__(self.message)


class CommandTimeoutError(Exception):
    def __init__(self, command: str):
        self.message = f"An error occurred while executing the '{command}', The command is timeout, The device don't return with any thing"
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


class SerialConnectError(Exception):
    def __init__(self, serial_port: str = ""):
        self.message = f"Program can't connect to {serial_port}"
        super().__init__(self.message)


class NoFontError(Exception):
    def __init__(self, font: str = ""):
        self.message = f"Program can't get {font} from your computer."
        super().__init__(self.message)
