from PyQt5 import QtCore, QtGui, QtWidgets
from src.factory.gui_factory import GUI_Factory
from src.communication import connection_manager
from src.json_handler import json_file
from src.pages.debug_page import DebugWindow
from src.pages.variable_config_page import VariableConfigurePage
from src.pages.os_configure_page import OSTemplateConfigurePage
from src.pages.result_page import ResultPage
from src.threads.data_collector_thread import DataCollectorThread
from src.style import main_style
import src.error as Error
from queue import Queue


class MainPage:

    def __init__(
        self,
        window_parent: QtWidgets.QMainWindow,
        connection_manager: connection_manager,
    ) -> None:
        self.main_widget = QtWidgets.QWidget(window_parent)
        self.main_grid = QtWidgets.QGridLayout(self.main_widget)
        self._window_parent = window_parent
        self.connection_manager = connection_manager
        self.json_handler = json_file()
        self.device_queue = Queue()
        self.json_handler.get_list_of_file()
        self.__setup_input_grid()
        self.__setup_connection_grid()
        self.__setup_json_grid()

        self.debug_button = GUI_Factory.create_button(
            "Open Debug Window", "popup_dialog_button", main_style
        )
        self.debug_button.clicked.connect(self.open_debug_window)
        self.main_grid.addWidget(self.debug_button, 3, 0)

    def get_widget(self):
        return self.main_widget

    def open_debug_window(self):
        """Open a debug window that captures printed output."""
        self.debug_window = DebugWindow(self._window_parent)
        self.debug_window.show()

    def __setup_input_grid(self):
        self.input_widget = GUI_Factory.create_widget(
            self.main_widget, "input_widget", main_style, 160, 825, 230
        )
        self.input_grid = QtWidgets.QGridLayout(self.input_widget)

        hostname_label = GUI_Factory.create_label(
            label_text="Hostname", obj_name="input_label"
        )

        self.hostname_input = GUI_Factory.create_lineedit(
            obj_name="input_lineedit", stylesheet=main_style
        )

        port_label = GUI_Factory.create_label(label_text="Port", obj_name="input_label")

        self.port_input = GUI_Factory.create_lineedit(
            obj_name="input_lineedit", stylesheet=main_style
        )
        self.port_input.setValidator(QtGui.QIntValidator(self.input_widget))
        self.port_input.setText("22")

        username_label = GUI_Factory.create_label(
            label_text="Username", obj_name="input_label", stylesheet=main_style
        )

        self.username_input = GUI_Factory.create_lineedit(
            obj_name="input_lineedit", stylesheet=main_style
        )

        password_label = GUI_Factory.create_label(
            label_text="Password", obj_name="input_label", stylesheet=main_style
        )

        self.password_input = GUI_Factory.create_lineedit(
            obj_name="input_lineedit", is_password=True
        )

        enable_password = GUI_Factory.create_label(
            label_text="Enable Password",
            obj_name="enable_pass_label",
        )

        self.enable_password_input = GUI_Factory.create_lineedit(
            obj_name="input_lineedit", is_password=True
        )

        self.connection_configure_button = GUI_Factory.create_button(
            "Connection Configure", "popup_dialog_button", main_style
        )
        self.connection_configure_button.clicked.connect(self.__show_input_dialog)
        self.input_grid.addWidget(hostname_label, 0, 0)
        self.input_grid.addWidget(self.hostname_input, 0, 1)
        self.input_grid.addWidget(port_label, 0, 2)
        self.input_grid.addWidget(self.port_input, 0, 3)
        self.input_grid.addWidget(username_label, 1, 0)
        self.input_grid.addWidget(self.username_input, 1, 1)
        self.input_grid.addWidget(password_label, 1, 2)
        self.input_grid.addWidget(self.password_input, 1, 3)
        self.input_grid.addWidget(enable_password, 2, 0)
        self.input_grid.addWidget(self.enable_password_input, 2, 1)
        self.input_grid.addWidget(
            self.connection_configure_button,
            2,
            2,
            1,
            2,
        )
        self.main_grid.addWidget(
            self.input_widget,
            0,
            0,
        )

    def __setup_connection_grid(self):
        self.connection_widget = GUI_Factory.create_widget(
            self.main_widget, "input_widget", main_style, 160, 825, 230
        )

        connection_top_widget = GUI_Factory.create_widget(
            self.main_widget, "sub_input_widget", main_style
        )

        connection_botton_widget = GUI_Factory.create_widget(
            self.main_widget, "sub_input_widget", main_style
        )

        connection_grid = QtWidgets.QGridLayout(self.connection_widget)
        connection_top_grid = QtWidgets.QGridLayout(connection_top_widget)
        connection_botton_grid = QtWidgets.QGridLayout(connection_botton_widget)

        self.connection_type_button_group = QtWidgets.QButtonGroup(self.main_widget)
        ssh_button = GUI_Factory.create_radio_button(
            "SSH", "./src/Assets/SSH.png", self.connection_type_button_group
        )
        ssh_button.setChecked(True)
        ssh_button.clicked.connect(lambda: self.__update_port_lineedit(22))
        telnet_button = GUI_Factory.create_radio_button(
            "Telnet", "./src/Assets/Telnet.png", self.connection_type_button_group
        )
        telnet_button.clicked.connect(lambda: self.__update_port_lineedit(23))

        serial_button = GUI_Factory.create_radio_button(
            "Serial", "./src/Assets/RS232.png", self.connection_type_button_group
        )
        self.connect_botton = GUI_Factory.create_button(
            "Connect", "popup_dialog_button", main_style
        )
        self.connect_botton.clicked.connect(self.__create_connection)

        serial_port_label = GUI_Factory.create_label(
            label_text="Serial Port",
            obj_name="connection_grid_label",
        )

        self.serial_port_combo_box = GUI_Factory.create_serial_combobox(
            self.connection_manager, width=300
        )

        baudrate_label = GUI_Factory.create_label(
            label_text="Baudrate",
            obj_name="connection_grid_label",
        )

        self.baudrate_combo_box = GUI_Factory.create_combobox(
            self.main_widget, font_size=22
        )
        self.baudrate_combo_box.setMinimumWidth(150)

        self.baudrate_combo_box.addItems(
            [
                "50",
                "75",
                "110",
                "134",
                "150",
                "200",
                "300",
                "600",
                "1200",
                "1800",
                "2400",
                "4800",
                "9600",
                "19200",
                "28800",
                "38400",
                "57600",
                "76800",
                "115200",
                "230400",
                "460800",
                "576000",
                "921600",
            ]
        )

        if self.connection_manager.baudrate in [
            int(self.baudrate_combo_box.itemText(i))
            for i in range(self.baudrate_combo_box.count())
        ]:
            self.baudrate_combo_box.setCurrentText(
                str(self.connection_manager.baudrate)
            )

        connection_top_grid.addWidget(ssh_button, 0, 0)
        connection_top_grid.addWidget(telnet_button, 0, 1)
        connection_top_grid.addWidget(serial_button, 0, 2)
        connection_top_grid.addWidget(self.connect_botton, 0, 3, 1, 3)
        connection_botton_grid.addWidget(
            serial_port_label,
            0,
            0,
        )
        connection_botton_grid.addWidget(self.serial_port_combo_box, 0, 1)
        connection_botton_grid.addWidget(
            baudrate_label,
            0,
            2,
        )
        connection_botton_grid.addWidget(self.baudrate_combo_box, 0, 3)
        connection_grid.addWidget(connection_top_widget, 0, 0)
        connection_grid.addWidget(connection_botton_widget, 1, 0)
        self.main_grid.addWidget(
            self.connection_widget,
            1,
            0,
        )

    def parse_hostnames(self, input_str):
        import re

        """Parse the input string for hostnames and handle IP ranges."""
        hostnames = []

        # Split by commas first
        parts = input_str.split(",")

        for part in parts:
            part = part.strip()

            # Check if the input is an IP-like structure
            if re.match(r"^\d+(\.\d+)*(-\d+)?(\.\d+)*$", part):
                # Handle IP ranges across multiple octets
                ranges = [r.split("-") for r in part.split(".")]
                octet_combinations = [[]]

                for r in ranges:
                    if len(r) == 2:
                        # If there's a range, expand it
                        start, end = int(r[0]), int(r[1])
                        new_combinations = []
                        for base in octet_combinations:
                            for i in range(start, end + 1):
                                new_combinations.append(base + [str(i)])
                        octet_combinations = new_combinations
                    else:
                        # Otherwise, just append the single value
                        new_combinations = []
                        for base in octet_combinations:
                            new_combinations.append(base + [r[0]])
                        octet_combinations = new_combinations

                # Construct the IP addresses from the octet combinations
                for combo in octet_combinations:
                    hostnames.append(".".join(combo))

            else:
                # If it's not an IP, treat it as a hostname
                hostnames.append(part)

        return hostnames

    def __setup_json_grid(self):
        # Create a new widget for the JSON grid layout
        json_widget = GUI_Factory.create_widget(
            self.main_widget, "input_widget", main_style, 160, 825, 230
        )
        json_grid = QtWidgets.QGridLayout(json_widget)

        # Create a label for JSON file selection
        json_label = GUI_Factory.create_label(
            "Select Device Configuration File:", "input_label"
        )
        json_label.setMinimumWidth(350)

        # Create a dropdown using ComboBoxWithDynamicArrow for JSON files
        self.json_file_dropdown = GUI_Factory.create_combobox(
            self.main_widget, font_size=22
        )
        self.json_file_dropdown.setObjectName("json_dropdown")

        # Create an instance of the json_file class and get the list of files

        self.os_version_dropdown = GUI_Factory.create_combobox(
            self.main_widget, font_size=22
        )

        # Populate the JSON dropdown with the list of files, set default value to Dell.json
        self.json_file_dropdown.addItems(
            sorted(self.json_handler.file_list)
        )  # Sort the file list
        if "Dell.json" in self.json_handler.file_list:
            self.json_file_dropdown.setCurrentText("Dell.json")
            self.__load_os_versions("Dell.json")

        # Create a label to show the OS version
        os_label = GUI_Factory.create_label("Select OS Version:", "input_label")

        # Create a dropdown for OS versions using ComboBoxWithDynamicArrow
        self.os_version_dropdown.setObjectName("os_version_dropdown")

        # Load the default JSON and populate the OS versions

        # Connect the JSON dropdown's change event to update the OS version dropdown
        self.json_file_dropdown.currentTextChanged.connect(self.update_os_versions)

        os_edit_button = GUI_Factory.create_button(
            "Edit OS Template", "popup_dialog_button", main_style
        )
        os_edit_button.clicked.connect(self.__show_os_template_edit_dialog)
        json_grid.addWidget(json_label, 0, 0)  # Row 0, Column 0
        json_grid.addWidget(self.json_file_dropdown, 0, 1)  # Row 0, Column 1
        json_grid.addWidget(os_label, 1, 0)  # Row 1, Column 0
        json_grid.addWidget(self.os_version_dropdown, 1, 1)  # Row 1, Column 1
        json_grid.addWidget(os_edit_button, 2, 0, 1, 2)
        # Add the json_widget (with the grid layout) to the main grid
        self.main_grid.addWidget(
            json_widget, 2, 0
        )  # Place in row 2, spanning 2 columns

    def __load_os_versions(self, json_file):
        """Load OS versions from the selected JSON file into the OS version dropdown."""
        try:
            self.json_handler.read_json_file(json_file)
            os_keys = self.json_handler.get_os_keys()
            self.os_version_dropdown.clear()  # Clear existing items
            self.os_version_dropdown.addItems(os_keys)  # Add new OS keys

            # Set the default selection to "os-10"
            if "os-10" in os_keys and json_file == "Dell.json":
                self.os_version_dropdown.setCurrentText("os-10")
        except Error.JsonFileNotFound as e:
            GUI_Factory.create_critical_message_box(
                self._window_parent,
                "File Not Found",
                f"The specified JSON file could not be found: {e}",
            )
            self.os_version_dropdown.clear()  # Clear choices on error
        except Error.InvalidJsonFile as e:
            GUI_Factory.create_critical_message_box(
                self._window_parent, "Invalid JSON", f"The JSON file is invalid: {e}"
            )
            self.os_version_dropdown.clear()  # Clear choices on error
        except Exception as e:
            GUI_Factory.create_critical_message_box(
                self._window_parent, "Error", f"An unexpected error occurred: {e}"
            )
            self.os_version_dropdown.clear()  # Clear choices on error

    def update_os_versions(self):
        """Update the OS version dropdown based on the selected JSON file."""
        selected_file = self.json_file_dropdown.currentText()
        if selected_file == "":
            return
        self.__load_os_versions(selected_file)  # Load OS versions for the selected file

    def __show_input_dialog(self):
        # Create and show the input dialog
        dialog = VariableConfigurePage(
            self.main_widget, self.connection_manager.get_curr_conf()
        )
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            user_input = dialog.get_input()
            self.connection_manager.set_parameters(user_input)

    def __show_os_template_edit_dialog(self):
        """Show the OS Template Edit Dialog and reload the JSON and OS version dropdowns upon closing."""
        dialog = OSTemplateConfigurePage(self.main_widget)

        # Execute the dialog and wait for it to close
        dialog.exec_()

        # Reload the JSON files and update the dropdowns
        self.json_handler.get_list_of_file()  # Refresh the file list
        self.update_json_file_dropdown()  # Update the JSON dropdown

        # Check if the dropdown is not empty before loading OS versions
        if self.json_file_dropdown.currentText() != "":
            self.update_os_versions()  # Refresh the OS versions based on the selected JSON file

    def update_json_file_dropdown(self):
        """Update the JSON file dropdown with the latest file list."""
        self.json_file_dropdown.clear()  # Clear existing items
        self.json_file_dropdown.addItems(
            sorted(self.json_handler.get_list_of_file())
        )  # Add sorted new file list

    def __update_port_lineedit(self, port):
        self.port_input.setText(str(port))  # Set the port input

    def __create_connection(self):
        """Main function to create a connection to the device."""
        # Check for required fields
        if not self.__check_required_fields():
            return
        # Split the hostnames input into a list
        hostnames_input = self.hostname_input.text().strip()
        hostnames = self.parse_hostnames(hostnames_input)
        if hostnames == []:
            GUI_Factory.create_critical_message_box(
                self._window_parent, "Error", "Please check your hostname"
            )
            return

        for hostname in hostnames:
            self.device_queue.put(hostname.strip())  # Add each hostname to the queue

        self.process_next_device()

    def process_next_device(self):
        """Process the next device in the queue."""
        if self.device_queue.empty():
            GUI_Factory.create_info_message_box(
                self._window_parent, "Done", "All devices processed."
            )
            return

        hostname = self.device_queue.get()  # Get the next hostname from the queue
        self.connected_hostname = hostname
        connection_params = {
            "hostname": hostname,
            "port": self.port_input.text().strip(),
            "username": self.username_input.text().strip(),
            "password": self.password_input.text().strip(),
            "enable_password": self.enable_password_input.text().strip(),
            "connection_type": self.connection_type_button_group.checkedButton().text(),
        }

        # Check if the connection type is Serial
        if connection_params["connection_type"] == "Serial":
            selected_serial_port = self.serial_port_combo_box.currentText()
            selected_baudrate = self.baudrate_combo_box.currentText()
            connection_params["serial_port"] = selected_serial_port
            connection_params["baudrate"] = selected_baudrate

        selected_os_version = self.__get_selected_os_version()
        command_dict_json = self.__get_command_dict(selected_os_version).copy()
        regex = (
            self.json_handler.get_regex(selected_os_version) or r"^\s*([\w-]+)(>|#)\s*$"
        )

        # Create the loading window
        self._loading_window = GUI_Factory.create_loading_window(
            self._window_parent,
            message=f"Connecting to {self.connected_hostname}, Please wait",
            width=600,
            terminate_callback=self.terminate_connections,
        )
        self._loading_window.show()

        # Create and start the new connection thread
        self.connection_thread = DataCollectorThread(
            params=connection_params,
            connection_manager=self.connection_manager,
            command_dict_json=command_dict_json,
            regex=regex,
            is_done_create_img=False,
        )

        # Connect signals
        self.connection_thread.connection_successful.connect(
            self.on_connection_successful
        )
        self.connection_thread.error_occurred.connect(self.on_error_occurred)
        self.connection_thread.data_collected.connect(self.on_data_collected)
        self.connection_thread.image_generated.connect(self.on_image_generated)
        self.connection_thread.finished.connect(self.on_device_process_finished)

        self.connection_thread.start()  # Start the thread

    def on_device_process_finished(self):
        """Handle completion of the current device's data collection."""
        # Hide the loading window after the data collection is done
        self._loading_window.accept()  # Close loading window
        # This method won't be called now; instead, the logic is in on_data_collected

    def on_connection_successful(self, params):
        """Handle successful connection."""
        print("Connection established successfully with parameters:", params)

        self._loading_window.update_label(
            f"Connected to {self.connected_hostname} , Collecting data..."
        )

    def on_data_collected(self, result):
        """Handle the collected data and show the result page."""
        if result is not None:
            self._loading_window.update_label(
                "Collecting data Done, Generating image..."
            )
            self._result_page = ResultPage(self._window_parent, result)
            self.connection_thread.set_result_page(self._result_page)

    def on_error_occurred(self, error_message):
        """Handle errors and show a message box."""
        GUI_Factory.create_critical_message_box(
            self._window_parent, "Connection Error", error_message
        )
        # Do not close the loading window, just update the status
        self._loading_window.update_label(
            "Error occurred. Moving to the next device..."
        )
        self._loading_window.setEnabled(True)  # Allow interaction after error

        # Continue to process the next device
        self.process_next_device()

    def on_image_generated(self):
        self._result_page.set_result_grid()
        self._result_page.exec_()  # Show the result page
        self.process_next_device()

    def __check_required_fields(self):
        """Check if all required fields are filled."""
        # Gather connection parameters
        connection_params = {
            "hostname": self.hostname_input.text().strip(),
            "port": self.port_input.text().strip(),
            "username": self.username_input.text().strip(),
            "password": self.password_input.text().strip(),
        }

        # If the selected connection type is Serial, ensure that the serial port and baudrate are checked too
        if self.connection_type_button_group.checkedButton().text() == "Serial":
            serial_port = self.serial_port_combo_box.currentText()
            baudrate = self.baudrate_combo_box.currentText()

            connection_params["serial_port"] = serial_port
            connection_params["baudrate"] = baudrate

        # Check for any missing required fields
        missing_fields = [key for key, value in connection_params.items() if not value]

        if missing_fields:
            # Alert for missing fields
            missing_fields_str = ", ".join(missing_fields)
            GUI_Factory.create_warning_message_box(
                self._window_parent,
                "Missing Input",
                f"The following fields are required: {missing_fields_str}",
            )

            return False  # Indicate that not all required fields are filled

        return True  # All required fields are filled

    def __get_selected_os_version(self):
        """Get the selected OS version from the dropdown and validate it."""
        selected_os_version = self.os_version_dropdown.currentText()

        if not selected_os_version:
            GUI_Factory.create_warning_message_box(
                self._window_parent,
                "Missing OS Version",
                "Please select an OS version before attempting to connect.",
            )
            return None  # Indicate that the selection was invalid

        return selected_os_version

    def __get_command_dict(self, os_version):
        """Retrieve the command dictionary for the selected OS version."""
        try:
            command_dict_json = self.json_handler.get_command_json(os_version)
            if command_dict_json is None:
                GUI_Factory.create_warning_message_box(
                    self._window_parent,
                    "Invalid OS Version",
                    f"No commands found for the selected OS version: {os_version}.",
                )
                return None  # Indicate that no commands were found
            return command_dict_json
        except Error.JsonOSTemplateError as e:
            GUI_Factory.create_critical_message_box(
                self._window_parent,
                "OS Template Error",
                f"Error processing commands for OS version: {str(e)}",
            )
            return None  # Indicate an error occurred

    def terminate_connections(self):
        """Terminate all connections and clear the queue."""
        # Implement logic to clear the device queue and stop running threads
        while not self.device_queue.empty():
            self.device_queue.get_nowait()  # Clear the queue

        # Optionally, if your DataCollectorThread has a way to stop, implement it here
        if self.connection_thread.isRunning():
            self.connection_thread.terminate()  # Assuming there's a terminate method
        GUI_Factory.create_info_message_box(
            self._window_parent, "Terminated", "All connections have been terminated."
        )
