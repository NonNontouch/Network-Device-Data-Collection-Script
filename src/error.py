class ErrorCommand(Exception):
    """_Error Class that handle when command given to device is returned error._"""

    def __init__(self, command: str, command_output: str):
        """_init the class._

        Args:
            command (str): _Command that is used._
            command_output (str): _Output of given command._
        """
        self.message = f"\nAn error occurred while executing the '{command}',\nIt gives output \n'{command_output}'"
        super().__init__(self.message)


class ErrorEnable_Password(Exception):
    def __init__(self, wrong_password: str):
        self.message = (
            f"\nAn error occurred while using given {wrong_password} password"
        )

        super().__init__(self.message)


class ErrorGetVLTNumber(Exception):
    def __init__(self):
        self.message = f"\nAn error occurred while trying to get VLT number"

        super().__init__(self.message)


class ConnectionError(Exception):
    def __init__(self, message: str = "The Connection variable is still null"):
        self.message = message
        super().__init__(self.message)


class CommandTimeoutError(Exception):
    def __init__(self, command: str):
        self.message = f"\nAn error occurred while executing the '{command}', The command is timeout, The device don't return with any thing"
        super().__init__(self.message)


class ConnectionLossConnect(Exception):
    def __init__(self, command: str):
        self.message = f"\nConnection was loss while executing the '{command}'"
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
        self.message = f"\nProgram can't connect to {serial_port}"
        super().__init__(self.message)


class NoFontError(Exception):
    def __init__(self, font: str = ""):
        self.message = f"\nProgram can't get {font} from your computer."
        super().__init__(self.message)


class InvalidJsonFile(Exception):
    def __init__(self, file: str = ""):
        self.message = f"\nProgram can read your {file}. Please check the file."
        super().__init__(self.message)


class WriteProbJonFile(Exception):
    def __init__(self, file: str = ""):
        self.message = f"\nProgram can write to your {file}. Please check the file."
        super().__init__(self.message)


class JsonFileNotFound(Exception):
    def __init__(self, file: str = ""):
        self.message = f"\nProgram can find your {file}. Please if the file is present."
        super().__init__(self.message)


class JsonOSTemplateError(Exception):
    def __init__(self, OS: str = ""):
        self.message = (
            f"\nThe program can't Procress the json template for {OS} you selected."
        )
        super().__init__(self.message)
