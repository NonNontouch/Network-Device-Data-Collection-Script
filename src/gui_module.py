import os
import subprocess
import sys
import tempfile
from PyQt5 import QtCore, QtGui, QtWidgets
from src.communication import connection_manager
from src.json_handler import json_file
import src.error as Error
from src.text_to_pic_module import text_to_pic


class GUI:
    main_style = """
    #main_window{
        background-color: #4D4D4D;
    }
    #input_label{
        border: 2px solid black;  
        border-radius: 10px;
        padding: 5px;
        background-color: #4D4D4D;
        color: white;
    }
    #enable_pass_label{
        border: 2px solid black;  
        border-radius: 10px;
        padding: 5px;
        background-color: #4D4D4D; 
        font-size: 18px;
        color: white;
    }
    #input_lineedit{
        border: 2px solid black;
        border-radius: 10px;
        padding: 5px;       
        min-width: 200px;
        background-color: #4D4D4D;  
        color:white;
    }
    #connection_grid_label{
        border: 2px solid black;  
        border-radius: 10px;
        padding: 5px;
        background-color: #696969;
        color: white;
    }
    #popup_dialog_button {
        background-color: #4CAF50;  /* Green background */
        color: white;  /* White text */
        border: 2px solid #4CAF50;  /* Green border */
        border-radius: 10px;  /* Rounded corners */
        padding: 10px 20px;  /* Padding inside the button */
        font-size: 16px;  /* Font size */
    }
    #popup_dialog_button:hover {
        background-color: #45a049;  /* Darker green on hover */
    }
    #popup_dialog_button:pressed {
        background-color: #388E3C;  /* Even darker green on press */
    }
    #input_widget{
        background-color: #252525;
        border: 2px solid black;
        border-radius: 10px;
        color: white;  
    }
    #sub_input_widget{
        background-color: #4D4D4D;
        border-radius: 10px;      
        border: 2px solid black;  
        padding: 10px;            
    }
    #input_label_configure_dialog{
        border: 2px solid black;  
        border-radius: 10px;
        padding: 3px;
        color: white;  
        background-color: #4D4D4D;    
        font: 16px;
        min-width: 160px
    }
    #input_lineedit_configure_dialog{
        border: 2px solid black;
        border-radius: 10px;
        padding: 3px;       
        min-width: 200px;
        color: white;  
        background-color: #4D4D4D;  
        font-size: 16px;
    }
    #label_banner{
       font-size: 18px; 
        font-weight: bold; 
        color: white; 
        padding: 10px; 
        background-color: #4D4D4D;
        border-radius: 10px;
        text-align: center; /* Center the text */
        width: 100%; /* Make the label take full width */
    }
    #acceptButton{
        background-color: #4CAF50;  /* Light green background */
        color: white;  /* White text */
        border: 2px solid #4CAF50;  /* Green border */
        border-radius: 10px;  /* Rounded corners */
        padding: 10px 20px;  /* Padding inside the button */
        font-size: 16px;  /* Font size */
    }
    #acceptButton:hover {
        background-color: #45a049;  /* Darker green on hover */
    }
    #acceptButton:pressed {
        background-color: #388E3C;  /* Even darker green on press */
    }
    #cancelButton {
        background-color: #f44336;  /* Light red background */
        color: white;  /* White text */
        border: 2px solid #f44336;  /* Red border */
        border-radius: 10px;  /* Rounded corners */
        padding: 10px 20px;  /* Padding inside the button */
        font-size: 16px;  /* Font size */
    }
    #cancelButton:hover {
        background-color: #e53935;  /* Darker red on hover */
    }
    #cancelButton:pressed {
        background-color: #c62828;  /* Even darker red on press */
    }
    QToolTip {
        font-size: 16px;  /* Smaller font size */
        padding: 5px;  /* Adjust padding */
        background-color: #4D4D4D;  /* Background color */
        color: white;  /* Text color */
    }
    """

    def __init__(self) -> None:
        try:
            self.App = QtWidgets.QApplication(sys.argv)
            font_id = QtGui.QFontDatabase.addApplicationFont(
                os.path.abspath("./src/Assets/BAHNSCHRIFT.ttf")
            )
            font_families = QtGui.QFontDatabase.applicationFontFamilies(font_id)
            default_text_font = QtGui.QFont(font_families[0], 18)
            self.App.setFont(default_text_font)

            self.Window = QtWidgets.QMainWindow()
            self.Window.setObjectName("main_window")
            self.Window.setStyleSheet(GUI.main_style)
            self.Window.setWindowTitle("Network Device Data Collection Script")

            icon_path = os.path.abspath("./src/Assets/AppIcon.png")
            if os.path.exists(icon_path):  # Check if the icon file exists
                self.App.setWindowIcon(QtGui.QIcon(icon_path))
                self.Window.setWindowIcon(
                    QtGui.QIcon(icon_path)
                )  # Set icon for the window
            else:
                print(f"Icon file not found: {icon_path}")

            self._connection_manager = connection_manager()
        except Exception as e:
            print(e)

    def setup_window(self):
        self.Main_Page = MainPage(self.Window, self._connection_manager)

        self.Window.setCentralWidget(self.Main_Page.get_widget())

        self.Window.show()
        GUI_Factory.center_window(self.Window)
        sys.exit(self.App.exec_())


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
        self.data_collection_in_progress = False
        self.__setup_input_grid()
        self.__setup_connection_grid()
        self.__setup_json_grid()

    def get_widget(self):
        return self.main_widget

    def __setup_input_grid(self):
        self.input_widget = GUI_Factory.create_widget(
            self.main_widget, "input_widget", GUI.main_style, 150, 800, 230
        )

        self.input_grid = QtWidgets.QGridLayout(self.input_widget)
        self.input_grid.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        hostname_label = GUI_Factory.create_label(
            label_text="Hostname", obj_name="input_label"
        )

        self.hostname_input = GUI_Factory.create_lineedit(
            obj_name="input_lineedit", stylesheet=GUI.main_style
        )

        port_label = GUI_Factory.create_label(label_text="Port", obj_name="input_label")

        self.port_input = GUI_Factory.create_lineedit(
            obj_name="input_lineedit", stylesheet=GUI.main_style
        )
        self.port_input.setValidator(QtGui.QIntValidator(self.input_widget))
        self.port_input.setText("22")

        username_label = GUI_Factory.create_label(
            label_text="Username", obj_name="input_label", stylesheet=GUI.main_style
        )

        self.username_input = GUI_Factory.create_lineedit(
            obj_name="input_lineedit", stylesheet=GUI.main_style
        )

        password_label = GUI_Factory.create_label(
            label_text="Password", obj_name="input_label", stylesheet=GUI.main_style
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
            "Connection Configure", "popup_dialog_button", GUI.main_style
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
            self.main_widget, "input_widget", GUI.main_style
        )

        connection_top_widget = GUI_Factory.create_widget(
            self.main_widget, "sub_input_widget", GUI.main_style
        )

        connection_botton_widget = GUI_Factory.create_widget(
            self.main_widget, "sub_input_widget", GUI.main_style
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
            "Connect", "popup_dialog_button", GUI.main_style
        )
        self.connect_botton.clicked.connect(self.__create_connection)

        self.comport_combo_box = ComboBoxWithDynamicArrow()
        connection_botton_grid.addWidget(self.comport_combo_box, 0, 1)
        self.comport_combo_box.setMinimumWidth(180)

        connection_botton_grid.addWidget(
            GUI_Factory.create_label(
                label_text="Baudrate",
                obj_name="connection_grid_label",
            ),
            0,
            2,
        )
        self.baudrate_combo_box = ComboBoxWithDynamicArrow()
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
        connection_botton_grid.addWidget(self.baudrate_combo_box, 0, 3)
        connection_top_grid.addWidget(ssh_button, 0, 0)
        connection_top_grid.addWidget(telnet_button, 0, 1)
        connection_top_grid.addWidget(serial_button, 0, 2)
        connection_top_grid.addWidget(self.connect_botton, 0, 3)
        connection_botton_grid.addWidget(
            GUI_Factory.create_label(
                label_text="Comport",
                obj_name="connection_grid_label",
            ),
            0,
            0,
        )
        connection_grid.addWidget(
            connection_top_widget, 0, 0, QtCore.Qt.AlignmentFlag.AlignHCenter
        )
        connection_grid.addWidget(
            connection_botton_widget, 1, 0, QtCore.Qt.AlignmentFlag.AlignHCenter
        )
        self.main_grid.addWidget(
            self.connection_widget,
            1,
            0,
        )

    def __setup_json_grid(self):
        # Create a new widget for the JSON grid layout
        json_widget = GUI_Factory.create_widget(self.main_widget, "input_widget")
        json_grid = QtWidgets.QGridLayout(json_widget)

        # Create a label for JSON file selection
        json_label = GUI_Factory.create_label(
            "Select Device Configuration File:", "input_label"
        )
        json_grid.addWidget(json_label, 0, 0)  # Row 0, Column 0

        # Create a dropdown using ComboBoxWithDynamicArrow for JSON files
        self.json_dropdown = ComboBoxWithDynamicArrow(self.main_widget)
        self.json_dropdown.setObjectName("json_dropdown")

        # Create an instance of the json_file class and get the list of files
        self.json_handler = json_file()
        self.json_handler.get_list_of_file()

        # Populate the JSON dropdown with the list of files, set default value to Dell.json
        self.json_dropdown.addItems(
            sorted(self.json_handler.file_list)
        )  # Sort the file list
        if "Dell.json" in self.json_handler.file_list:
            self.json_dropdown.setCurrentText("Dell.json")

        json_grid.addWidget(self.json_dropdown, 0, 1)  # Row 0, Column 1

        # Create a label to show the OS version
        os_label = GUI_Factory.create_label("Select OS Version:", "input_label")
        json_grid.addWidget(os_label, 1, 0)  # Row 1, Column 0

        # Create a dropdown for OS versions using ComboBoxWithDynamicArrow
        self.os_version_dropdown = ComboBoxWithDynamicArrow(self.main_widget)
        self.os_version_dropdown.setObjectName("os_version_dropdown")
        json_grid.addWidget(self.os_version_dropdown, 1, 1)  # Row 1, Column 1

        # Load the default JSON and populate the OS versions
        self.__load_os_versions("Dell.json")

        # Connect the JSON dropdown's change event to update the OS version dropdown
        self.json_dropdown.currentTextChanged.connect(self.update_os_versions)

        json_edit_button = GUI_Factory.create_button(
            "Connection Configure", "popup_dialog_button", GUI.main_style
        )
        json_grid.addWidget(json_edit_button, 2, 0, 2, 2)

        # Add the json_widget (with the grid layout) to the main grid
        self.main_grid.addWidget(
            json_widget, 2, 0, 1, 2
        )  # Place in row 2, spanning 2 columns

    def __load_os_versions(self, json_file):
        """Load OS versions from the selected JSON file into the OS version dropdown."""
        try:
            self.json_handler.read_json_file(json_file)
            os_keys = self.json_handler.get_os_keys()
            self.os_version_dropdown.clear()  # Clear existing items
            self.os_version_dropdown.addItems(os_keys)  # Add new OS keys

            # Set the default selection to "os-10"
            if "os-10" in os_keys:
                self.os_version_dropdown.setCurrentText("os-10")
        except Error.JsonFileNotFound as e:
            QtWidgets.QMessageBox.critical(
                self._window_parent,
                "File Not Found",
                f"The specified JSON file could not be found: {e}",
            )
            self.os_version_dropdown.clear()  # Clear choices on error
        except Error.InvalidJsonFile as e:
            QtWidgets.QMessageBox.critical(
                self._window_parent,
                "Invalid JSON",
                f"The JSON file is invalid: {e}",
            )
            self.os_version_dropdown.clear()  # Clear choices on error
        except Exception as e:
            QtWidgets.QMessageBox.critical(
                self._window_parent,
                "Error",
                f"An unexpected error occurred: {e}",
            )
            self.os_version_dropdown.clear()  # Clear choices on error

    def update_os_versions(self):
        """Update the OS version dropdown based on the selected JSON file."""
        selected_file = self.json_dropdown.currentText()
        self.__load_os_versions(selected_file)  # Load OS versions for the selected file

    def __show_input_dialog(self):
        # Create and show the input dialog
        dialog = VariableConfigurePage(self.main_widget)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            user_input = dialog.get_input()
            self.connection_manager.set_parameters(user_input)

    def __update_port_lineedit(self, port):
        self.port_input.setText(str(port))  # Set the port input

    def __create_connection(self):
        """Main function to create a connection to the device."""
        # First, check for required fields
        if not self.__check_required_fields():
            return  # Alert will be shown in the __check_required_fields method

        selected_os_version = self.__get_selected_os_version()
        if selected_os_version is None:
            return  # User was alerted

        command_dict_json = self.__get_command_dict(selected_os_version)
        if command_dict_json is None:
            return  # User was alerted

        # Create and show the loading window
        loading_window = GUI_Factory.create_loading_window(self._window_parent)
        loading_window.show()

        try:
            # Attempt to connect to the device
            self.__connect_to_device()  # Connect to the device

            # Start the data collection thread after successful connection
            self.data_collector_thread = DataCollectorThread(
                self.connection_manager, command_dict_json
            )

            # Connect signals to handle data collection and errors
            self.data_collector_thread.data_collected.connect(self.on_data_collected)
            self.data_collector_thread.error_occurred.connect(self.on_error_occurred)
            self.data_collector_thread.finished.connect(
                loading_window.accept
            )  # Close loading on thread finish

            self.data_collector_thread.start()  # Start the thread
        except Exception as e:
            loading_window.accept()  # Close loading window if there's an error
            print("alert in create connection")
            GUI_Factory.create_alert_window(
                self._window_parent, str(e)
            )  # Show alert for connection error

    def on_data_collected(self, result):
        """Handle the collected data and show the result page."""
        if result is not None:
            self._result = result
            self._show_result_page()  # Show the result page

    def on_error_occurred(self, error_message):
        """Handle errors and show a message box."""
        QtWidgets.QMessageBox.critical(
            self._window_parent, "Connection Error", error_message
        )

    def __check_required_fields(self):
        """Check if all required fields are filled."""
        connection_params = {
            "hostname": self.hostname_input.text().strip(),
            "port": self.port_input.text().strip(),
            "username": self.username_input.text().strip(),
            "password": self.password_input.text().strip(),
        }

        missing_fields = [key for key, value in connection_params.items() if not value]

        if missing_fields:
            # Alert for missing fields
            missing_fields_str = ", ".join(missing_fields)
            QtWidgets.QMessageBox.warning(
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
            QtWidgets.QMessageBox.warning(
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
                QtWidgets.QMessageBox.warning(
                    self._window_parent,
                    "Invalid OS Version",
                    f"No commands found for the selected OS version: {os_version}.",
                )
                return None  # Indicate that no commands were found
            return command_dict_json
        except Error.JsonOSTemplateError as e:
            QtWidgets.QMessageBox.critical(
                self._window_parent,
                "OS Template Error",
                f"Error processing commands for OS version: {str(e)}",
            )
            return None  # Indicate an error occurred

    def __connect_to_device(self):
        # Gather values from all QLineEdit inputs
        connection_params = {
            "hostname": self.hostname_input.text().strip(),
            "port": self.port_input.text().strip(),
            "username": self.username_input.text().strip(),
            "password": self.password_input.text().strip(),
            "enable_password": self.enable_password_input.text().strip(),
        }
        missing_fields = []
        for key, value in connection_params.items():
            if key != "enable_password" and not value:  # Check if the value is empty
                missing_fields.append(key)

        if missing_fields:
            # Create an alert for missing variables
            missing_fields_str = ", ".join(missing_fields)
            QtWidgets.QMessageBox.warning(
                self._window_parent,
                "Missing Input",
                f"The following fields are required: {missing_fields_str}",
            )
            return  # Exit the method if there are missing fields
        self.connection_manager.set_parameters(connection_params)
        try:
            if (
                self.connection_type_button_group.checkedButton()
                == self.connection_type_button_group.buttons()[0]
            ):  # SSH
                self.connection_manager.set_ssh_connection()
            elif (
                self.connection_type_button_group.checkedButton()
                == self.connection_type_button_group.buttons()[1]
            ):  # Telnet
                self.connection_manager.set_telnet_connection()
            elif (
                self.connection_type_button_group.checkedButton()
                == self.connection_type_button_group.buttons()[2]
            ):  # Serial
                self.connection_manager.set_serial_connection()

            # Optionally, print or log the successful connection status
            print(
                "Connection established successfully with parameters:",
                connection_params,
            )

        except Exception as e:
            print("alert in connect to device")
            GUI_Factory.create_alert_window(self._window_parent, str(e))
            raise e

    def __send_commands(self, command_dict_json):
        """Send the commands to the connection manager."""
        try:
            result = self.connection_manager.send_list_command(command_dict_json)
            print(f"Commands sent successfully for OS version.")
            return result
        except Error.ConnectionError as e:
            QtWidgets.QMessageBox.critical(
                self._window_parent,
                "Connection Error",
                f"Error connecting to the device: {str(e)}",
            )
        except Exception as e:
            QtWidgets.QMessageBox.critical(
                self._window_parent,
                "Unexpected Error",
                f"An unexpected error occurred: {str(e)}",
            )

    def _show_result_page(self):
        """Show the result page dialog."""
        """ dummy_results = {
            "Tetminal Length 0": "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
            "show running-configuration": "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
            "show interface status": "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
            "show cpu usage": "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
            "show memory": "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
            "show system status": "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
            "show vlt number": "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
            "show vlt status": "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
            "show tech-support": "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
            "Tetminal Length 0 1": "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
            "show running-configuration 1": "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
            "show interface status 1": "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
            "show cpu usage 1": "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
            "show memory 1": "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
            "show system status 1": "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
            "show vlt number 1": "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
            "show vlt status 1": "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
            "show tech-support 1": "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
        }"""
        dialog = ResultPage(self._window_parent, self._result)
        dialog.exec_()  # Show the result page


class VariableConfigurePage:

    def __init__(self, widget_parent: QtWidgets.QMainWindow) -> None:
        # Create a QDialog instance
        self._widget_parrent = widget_parent
        self.varialbe_configure_page_dialog = QtWidgets.QDialog(widget_parent)
        self.verialbe_configure_page_grid_layout = QtWidgets.QGridLayout(
            self.varialbe_configure_page_dialog
        )
        self.varialbe_configure_page_dialog.setWindowTitle("Input Dialog")
        self.__set_ip_input_variable_grid()
        self.__set_serial_input_grid()
        self._set_button_grid()

    def __set_ip_input_variable_grid(self):
        self.input_widget = GUI_Factory.create_widget(
            self._widget_parrent, "input_widget", GUI.main_style, 220, 500, 400
        )

        self.ip_variable_grid = QtWidgets.QGridLayout(self.input_widget)
        self.ip_variable_grid.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)

        banner_label = GUI_Factory.create_label(
            "IP Timer Configuration", "label_banner", GUI.main_style
        )

        login_wait_label = GUI_Factory.create_label(
            label_text="Login Wait Time",
            obj_name="input_label_configure_dialog",
        )
        self.login_wait_input = GUI_Factory.create_lineedit(
            obj_name="input_lineedit_configure_dialog",
            placeholder_text="Default 3",
        )
        self.login_wait_input.setValidator(QtGui.QDoubleValidator(self.input_widget))

        banner_timeout_label = GUI_Factory.create_label(
            label_text="Banner Timeout",
            obj_name="input_label_configure_dialog",
        )
        self.banner_timeout_input = GUI_Factory.create_lineedit(
            obj_name="input_lineedit_configure_dialog",
            placeholder_text="Default 15",
        )
        self.banner_timeout_input.setValidator(
            QtGui.QDoubleValidator(self.input_widget)
        )

        command_retriesdelay_label = GUI_Factory.create_label(
            label_text="Command Timeout",
            obj_name="input_label_configure_dialog",
        )
        self.command_retriesdelay_input = GUI_Factory.create_lineedit(
            obj_name="input_lineedit_configure_dialog",
            placeholder_text="Default 4",
        )
        self.command_retriesdelay_input.setValidator(
            QtGui.QDoubleValidator(self.input_widget)
        )

        command_maxretries_label = GUI_Factory.create_label(
            label_text="Command Max Retries",
            obj_name="input_label_configure_dialog",
        )
        self.command_maxretries_input = GUI_Factory.create_lineedit(
            obj_name="input_lineedit_configure_dialog",
            placeholder_text="Default 4",
        )
        self.command_maxretries_input.setValidator(
            QtGui.QDoubleValidator(self.input_widget)
        )

        # Add New Widgets to Grid
        self.ip_variable_grid.addWidget(banner_label, 0, 0, 1, 2)

        self.ip_variable_grid.addWidget(login_wait_label, 1, 0)
        self.ip_variable_grid.addWidget(self.login_wait_input, 1, 1)
        self.ip_variable_grid.addWidget(banner_timeout_label, 2, 0)
        self.ip_variable_grid.addWidget(self.banner_timeout_input, 2, 1)
        self.ip_variable_grid.addWidget(command_retriesdelay_label, 3, 0)
        self.ip_variable_grid.addWidget(self.command_retriesdelay_input, 3, 1)
        self.ip_variable_grid.addWidget(command_maxretries_label, 4, 0)
        self.ip_variable_grid.addWidget(self.command_maxretries_input, 4, 1)
        self.verialbe_configure_page_grid_layout.addWidget(
            self.input_widget,
            0,
            0,
        )

    def __set_serial_input_grid(self):
        self.serial_widget = GUI_Factory.create_widget(
            self._widget_parrent, "input_widget", GUI.main_style, 180, 500, 400
        )

        self.serial_variable_grid = QtWidgets.QGridLayout(self.serial_widget)
        banner_label = GUI_Factory.create_label(
            "Serial Configuration", "label_banner", GUI.main_style
        )
        bytesize_label = GUI_Factory.create_label(
            label_text="Bytesize",
            obj_name="input_label_configure_dialog",
        )
        self.bytesize_input = GUI_Factory.create_lineedit(
            obj_name="input_lineedit_configure_dialog",
            placeholder_text="Default 8",
        )
        self.bytesize_input.setValidator(QtGui.QIntValidator(self.serial_widget))

        parity_label = GUI_Factory.create_label(
            label_text="Parity",
            obj_name="input_label_configure_dialog",
        )
        self.parity_input = GUI_Factory.create_lineedit(
            obj_name="input_lineedit_configure_dialog",
            placeholder_text="Default N",
        )
        parity_info = GUI_Factory.create_info_icon(
            icon_path="./src/Assets/info.png",
            tooltip_text=(
                "Select a parity option:\n"
                "E: Even parity (serial.PARITY_EVEN)\n"
                "N: No parity (serial.PARITY_NONE)\n"
                "M: Mark parity (serial.PARITY_MARK)\n"
                "O: Odd parity (serial.PARITY_ODD)\n"
                "S: Space parity (serial.PARITY_SPACE)"
            ),
            obj_name="info_icon",
        )

        stopbits_label = GUI_Factory.create_label(
            label_text="Stopbits",
            obj_name="input_label_configure_dialog",
        )
        self.stopbits_input = GUI_Factory.create_lineedit(
            obj_name="input_lineedit_configure_dialog",
            placeholder_text="Default 1",
        )
        self.stopbits_input.setValidator(QtGui.QDoubleValidator(self.serial_widget))

        self.serial_variable_grid.addWidget(banner_label, 0, 0, 1, 3)
        self.serial_variable_grid.addWidget(bytesize_label, 1, 0)
        self.serial_variable_grid.addWidget(self.bytesize_input, 1, 1, 1, 2)
        self.serial_variable_grid.addWidget(parity_label, 2, 0)
        self.serial_variable_grid.addWidget(self.parity_input, 2, 1)
        self.serial_variable_grid.addWidget(parity_info, 2, 2)
        self.serial_variable_grid.addWidget(stopbits_label, 3, 0)
        self.serial_variable_grid.addWidget(self.stopbits_input, 3, 1, 1, 2)
        self.verialbe_configure_page_grid_layout.addWidget(
            self.serial_widget,
            1,
            0,
        )

    def _set_button_grid(self):
        self.button_widget = GUI_Factory.create_widget(
            self._widget_parrent, "input_widget", GUI.main_style, 40, 500, 100
        )

        self.button_grid = QtWidgets.QGridLayout(self.button_widget)

        self.apply_button = GUI_Factory.create_button(
            "Apply", "acceptButton", GUI.main_style
        )
        self.cancel_button = GUI_Factory.create_button(
            "Cancle", "cancelButton", GUI.main_style
        )

        self.button_grid.addWidget(self.apply_button, 0, 0)
        self.button_grid.addWidget(self.cancel_button, 0, 1)
        # Connect buttons
        self.apply_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

        self.verialbe_configure_page_grid_layout.addWidget(self.button_widget, 2, 0)

    def exec_(self):
        return self.varialbe_configure_page_dialog.exec_()

    def accept(self):
        self.result = QtWidgets.QDialog.Accepted
        self.varialbe_configure_page_dialog.accept()

    def reject(self):
        self.result = QtWidgets.QDialog.Rejected
        self.varialbe_configure_page_dialog.reject()

    def get_input(self):
        return {
            "login_wait_time": self.login_wait_input.text(),
            "banner_timeout": self.banner_timeout_input.text(),
            "command_retriesdelay": self.command_retriesdelay_input.text(),
            "command_max_retries": self.command_maxretries_input.text(),
            "bytesize": self.bytesize_input.text(),
            "parity": self.parity_input.text(),
            "stopbits": self.stopbits_input.text(),
        }

    def result(self):
        return self.result


class DataCollectorThread(QtCore.QThread):
    data_collected = QtCore.pyqtSignal(dict)
    error_occurred = QtCore.pyqtSignal(str)

    def __init__(self, connection_manager, command_dict_json):
        super().__init__()
        self.connection_manager = connection_manager
        self.command_dict_json = command_dict_json

    def run(self):
        """Run the connection and command sending in a separate thread."""
        try:
            result = self.connection_manager.send_list_command(self.command_dict_json)
            self.data_collected.emit(result)  # Emit the collected data
        except Exception as e:
            self.error_occurred.emit(str(e))  # Emit error message


class ResultPage:
    def __init__(self, widget_parent, result: dict) -> None:
        self._widget_parent = widget_parent
        self.result_page_dialog = QtWidgets.QDialog(widget_parent)
        self.result_page_dialog.setWindowTitle("Result Viewer")
        self._result = result
        self.text_to_picture = text_to_pic()  # Instance of text_to_pic
        self.temp_image_paths = []  # To store paths of temp images
        self.__set_result_grid()

    def __set_result_grid(self):
        # Create the main grid layout
        main_grid = QtWidgets.QGridLayout(self._widget_parent)

        # Create a widget to hold the results
        result_widget = GUI_Factory.create_widget(None, "input_widget", GUI.main_style)
        results_layout = QtWidgets.QGridLayout(result_widget)

        # Create a scroll area
        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(
            result_widget
        )  # Set the result widget as the scroll area content

        # Populate the results content with buttons for each result
        i = 0
        for title, result in self._result.items():
            sub_widget = GUI_Factory.create_widget(
                self._widget_parent, "single_result_widget", GUI.main_style, 400, 100
            )
            sub_grid = QtWidgets.QGridLayout(sub_widget)
            command_banner = GUI_Factory.create_label(
                f"{title}", "label_banner", GUI.main_style
            )
            sub_grid.addWidget(command_banner, 0, 0, 1, 2)
            # Create a temporary file to hold the generated image
            temp_image_path = self.generate_image(result)

            # Create a button to preview the image
            preview_button = GUI_Factory.create_button(
                f"Preview {title} Image", "", GUI.main_style
            )
            preview_button.clicked.connect(
                lambda checked, img_path=temp_image_path: self.preview_image(img_path)
            )
            sub_grid.addWidget(preview_button, 1, 0, 1, 2)

            # Create a button to save the image
            save_image_button = QtWidgets.QPushButton(f"Save {title} Image")
            save_image_button.clicked.connect(
                lambda checked, img_path=temp_image_path, title=title: self.save_image(
                    img_path, title
                )
            )
            sub_grid.addWidget(save_image_button, 2, 0)

            # Create a button to save the text
            save_text_button = QtWidgets.QPushButton(f"Save {title} Text")
            save_text_button.clicked.connect(
                lambda checked, text=result, title=title: self.save_text(text, title)
            )
            sub_grid.addWidget(save_text_button, 2, 1)
            results_layout.addWidget(sub_widget, i, 0)
            i += 1

        # Add the scroll area to the main grid layout
        main_grid.addWidget(scroll_area, 0, 0)

        # Set the main layout to the dialog
        self.result_page_dialog.setLayout(main_grid)

    def save_text(self, text, title):
        """Open a file dialog to save the text."""
        options = QtWidgets.QFileDialog.Options()
        # Get the current working directory
        default_path = os.getcwd()
        # Set default file name
        default_file_name = f"{title}.txt"
        file_path, _ = QtWidgets.QFileDialog.getSaveFileName(
            self.result_page_dialog,
            f"Save {title} Text",
            os.path.join(default_path, default_file_name),
            "Text Files (*.txt);;All Files (*)",
            options=options,
        )
        if file_path:
            with open(file_path, "w") as file:
                file.write(text)  # Save the text to the selected path

    def save_image(self, image_path, title):
        """Open a file dialog to save the image."""
        options = QtWidgets.QFileDialog.Options()
        # Get the current working directory
        default_path = os.getcwd()
        # Set default file name based on the title
        default_file_name = f"{title}.png"  # Assuming you want to save it as a PNG
        file_path, _ = QtWidgets.QFileDialog.getSaveFileName(
            self.result_page_dialog,
            f"Save {title} Image",
            os.path.join(default_path, default_file_name),
            "Images (*.png *.jpg *.bmp);;All Files (*)",
            options=options,
        )
        if file_path:
            # Copy the temporary image to the new location
            with open(image_path, "rb") as src_file:
                with open(file_path, "wb") as dst_file:
                    dst_file.write(
                        src_file.read()
                    )  # Save the image to the selected path

    def generate_image(self, text: str) -> str:
        """Generate an image from the given text and return the file path."""
        image = self.text_to_picture.create_text_image(text)

        # Create a temporary file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
        temp_file_path = temp_file.name

        # Save the image to the temporary file
        image.save(temp_file_path)  # Save the image
        temp_file.close()  # Close the temp file so it can be accessed later

        # Store the temp file path for cleanup
        self.temp_image_paths.append(temp_file_path)

        return temp_file_path  # Return the path to the temporary image

    def cleanup_temp_images(self):
        """Delete all temporary image files created."""
        for path in self.temp_image_paths:
            if os.path.exists(path):
                os.remove(path)

    def preview_image(self, image_path: str):
        """Open the image using the default image viewer."""
        # Check if the image file exists
        if os.path.exists(image_path):
            try:
                # subprocess.Popen(["xdg-open", image_path], shell=True)  # For Linux
                subprocess.Popen(["open", image_path])  # For macOS
                # subprocess.Popen(['start', image_path], shell=True)  # For Windows
            except Exception as e:
                QtWidgets.QMessageBox.warning(
                    self._widget_parent, "Error", f"Failed to open image: {str(e)}"
                )
        else:
            QtWidgets.QMessageBox.warning(
                self._widget_parent,
                "File Not Found",
                f"The specified image file does not exist: {image_path}",
            )

    def exec_(self):
        """Show the result dialog and cleanup temp images on close."""
        result = self.result_page_dialog.exec_()
        self.cleanup_temp_images()  # Clean up temp images when dialog is closed
        return result


class GUI_Factory:

    @staticmethod
    def center_window(Window: QtWidgets.QWidget):
        window_geometry = Window.frameGeometry()

        # Get the center point of the parent window
        if isinstance(Window.parent(), QtWidgets.QMainWindow):
            parent_geometry = Window.parent().frameGeometry()
            center_point = parent_geometry.center()
        else:
            # Fallback to screen center if no parent is a QMainWindow
            center_point = QtWidgets.QDesktopWidget().availableGeometry().center()

        # Move the center of the window's geometry to the center point
        window_geometry.moveCenter(center_point)

        # Move the top-left point of the window to the top-left of the adjusted geometry
        Window.move(window_geometry.topLeft())

    @staticmethod
    def create_label(label_text: str, obj_name: str, stylesheet: str = ""):
        temp_label = QtWidgets.QLabel(text=label_text)
        temp_label.setObjectName(obj_name)
        if stylesheet:
            temp_label.setStyleSheet(stylesheet)
        return temp_label

    @staticmethod
    def create_lineedit(
        obj_name: str,
        stylesheet: str = "",
        is_password=False,
        placeholder_text: str = "",
    ):
        temp_lineedit = QtWidgets.QLineEdit()
        temp_lineedit.setObjectName(obj_name)
        if stylesheet:
            temp_lineedit.setStyleSheet(stylesheet)
        if is_password:
            temp_lineedit.setEchoMode(QtWidgets.QLineEdit.Password)
        if placeholder_text:
            temp_lineedit.setPlaceholderText(placeholder_text)
        return temp_lineedit

    @staticmethod
    def create_widget(
        parent,
        obj_name,
        stylesheet="",
        min_height=None,
        min_width=None,
        max_height=None,
        max_width=None,
    ):
        widget = QtWidgets.QWidget(parent)
        widget.setObjectName(obj_name)
        if stylesheet:
            widget.setStyleSheet(stylesheet)
        if min_height:
            widget.setMinimumHeight(min_height)
        if min_width:
            widget.setMinimumWidth(min_width)
        if max_height:
            widget.setMaximumHeight(max_height)
        if max_width:
            widget.setMaximumWidth(max_width)
        return widget

    @staticmethod
    def create_button(text: str, obj_name: str, stylesheet: str = ""):
        temp_button = QtWidgets.QPushButton(text)
        temp_button.setObjectName(obj_name)
        temp_button.setStyleSheet(stylesheet)
        temp_button.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        return temp_button

    @staticmethod
    def create_radio_button(text, image_path, botton_group):
        # Create a QRadioButton
        radio_button = QtWidgets.QRadioButton(text)

        # Load and set the image for the radio button
        icon = QtGui.QIcon(image_path)
        radio_button.setIcon(icon)
        radio_button.setIconSize(QtCore.QSize(24, 24))  # Set the size of the icon
        radio_button.setStyleSheet(
            """
            QRadioButton {
            background-color: #696969; 
            border-radius: 10px;
            padding: 5px;
            border: none;
            color: white;
            }
            QRadioButton::indicator {
                width: 16px;
                height: 16px;
                border: 2px solid black;
                background-color: white;  
            } 
            QRadioButton::indicator:checked {
                background-color: white; 
                border: 2px solid black;
                background-image: url(./src/Assets/checkmark.png); 
                background-repeat: no-repeat;
                background-position: center;
            }
        """
        )
        radio_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        # Add the radio button to the button group
        botton_group.addButton(radio_button)
        return radio_button

    @staticmethod
    def create_info_icon(
        icon_path: str,
        tooltip_text: str,
        obj_name: str,
        stylesheet: str = "",
        size=(24, 24),
    ):  # Default size is 16x16
        # Create the QLabel for the icon
        info_icon = QtWidgets.QLabel()
        if icon_path:
            pixmap = QtGui.QPixmap(icon_path).scaled(
                size[0], size[1], QtCore.Qt.AspectRatioMode.KeepAspectRatio
            )  # Resize the icon
            if stylesheet:
                info_icon.setStyleSheet(stylesheet)
            info_icon.setPixmap(pixmap)  # Set the resized pixmap
            info_icon.setToolTip(tooltip_text)  # Set the tooltip with information
            info_icon.setAlignment(
                QtCore.Qt.AlignmentFlag.AlignRight
            )  # Align to the right
            info_icon.setObjectName(obj_name)

        return info_icon

    @staticmethod
    def create_alert_window(parrent: QtWidgets.QMainWindow, message: str):
        return QtWidgets.QMessageBox.critical(
            parrent,
            "Unexpected Error",
            f"An unexpected error occurred: {str(message)}",
        )

    @staticmethod
    def create_loading_window(
        parent=None,
        width: int = 400,
        height: int = 150,
        message="Processing, please wait...",
    ):
        """Create a loading window with a progress bar."""
        loading_window = QtWidgets.QDialog(parent)
        loading_window.setWindowTitle("Loading")
        loading_window.setModal(True)
        loading_window.setFixedSize(width, height)

        layout = QtWidgets.QVBoxLayout(loading_window)
        label = QtWidgets.QLabel(message)
        progress = QtWidgets.QProgressBar()
        progress.setRange(0, 0)  # Indeterminate progress
        layout.addWidget(label)
        layout.addWidget(progress)

        return loading_window


class ComboBoxWithDynamicArrow(QtWidgets.QComboBox):
    def __init__(self, parent=None):
        super(ComboBoxWithDynamicArrow, self).__init__(parent)
        self.combobox_style = """ 
        QComboBox {
            background-color: #696969; /* Dark background color */
            border: 1px solid #2F2F2F;
            border-radius: 5px;
            padding: 5px;
            color: white; 
            font-size: 18px;
        }

        QComboBox::drop-down {
            subcontrol-origin: padding;
            subcontrol-position: top right;
            width: 25px;
            border-left-width: 1px;
            border-left-color: #2F2F2F;
            border-left-style: solid;
            border-top-right-radius: 3px;
            background: #3A3A3A; /* Darker drop-down background */
            
        }

        QComboBox QAbstractItemView {
            border: 1px solid #2F2F2F;
            background-color: #2F2F2F; /* Darker background for the drop-down list */
            selection-background-color: #3A3A3A; /* Selection background color */
            selection-color: white; /* Selection text color */
            color: white;
            min-height: 15px;
        }    
        QComboBox::down-arrow {
                image: url(./src/Assets/arrow_down.png); 
                width: 15px;
                height: 15px;
            }"""
        # Set the default arrow (down)
        self.setStyleSheet(self.combobox_style)

        # Connect signals for popup and close
        self.view().window().installEventFilter(self)
        self.popup_open = False

    def eventFilter(self, source, event):
        if event.type() == event.Show:
            self.set_arrow_up()
        elif event.type() == event.Hide:
            self.set_arrow_down()
        return super(ComboBoxWithDynamicArrow, self).eventFilter(source, event)

    def set_arrow_up(self):
        self.setStyleSheet(self.combobox_style.replace("arrow_down", "arrow_up"))

    def set_arrow_down(self):
        self.setStyleSheet(self.combobox_style)
