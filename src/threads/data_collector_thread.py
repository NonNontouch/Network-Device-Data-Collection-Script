from PyQt5 import QtCore

from src.communication import connection_manager


class DataCollectorThread(QtCore.QThread):
    connection_successful = QtCore.pyqtSignal(dict)
    data_collected = QtCore.pyqtSignal(dict)
    image_generated = QtCore.pyqtSignal()
    error_occurred = QtCore.pyqtSignal(str)

    def __init__(
        self,
        params: dict,
        connection_manager: connection_manager,
        command_dict_json: dict,
        is_done_create_img: bool,
    ):
        super().__init__()
        self.connection_manager = connection_manager
        self.command_dict_json = command_dict_json
        self.params = params
        self.is_done_create_img = is_done_create_img
        self.result_page = None

    def run(self):
        try:
            self.connection_manager.set_parameters(self.params)

            # Set the connection type based on the parameters
            if self.params.get("connection_type") == "SSH":
                self.connection_manager.set_ssh_connection()
            elif self.params.get("connection_type") == "Telnet":
                self.connection_manager.set_telnet_connection()
            elif self.params.get("connection_type") == "Serial":
                self.connection_manager.set_serial_connection()

            # Emit success signal
            self.connection_successful.emit(self.params)
            result = self.connection_manager.send_list_command(self.command_dict_json)
            self.data_collected.emit(result)  # Emit the collected data
            from time import sleep

            while True:
                sleep(0.1)
                if self.result_page != None:
                    self.result_page.generate_all_image()
                    self.image_generated.emit()
                    break
            self.quit()
        except Exception as e:
            print(e)
            self.error_occurred.emit(str(e))  # Emit error message
        """Run the connection and command sending in a separate thread."""

    def set_result_page(self, result_page):
        self.result_page = result_page
