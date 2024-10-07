import os
import platform
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
        text-align: center;
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
    #result_button_preview{
        background-color:  #2196F3;  /* Sky blue background */
        color: white;  /* White text */
        border: 2px solid  #2196F3 ;  /* Sky blue border */
        border-radius: 10px;  /* Rounded corners */
        padding: 10px 20px;  /* Padding inside the button */
        font-size: 16px;  /* Font size */
    }
    #result_button_save_image{
        background-color:  #FFA500;  /* orange background */
        color: white;  /* White text */
        border: 2px solid  #2196F3 ;  /* orange border */
        border-radius: 10px;  /* Rounded corners */
        padding: 10px 20px;  /* Padding inside the button */
        font-size: 16px;  /* Font size */
    }
    #result_button_save_text{
        background-color:  #ADD8E6;  /* light blue background */
        color: black;  /* White text */
        border: 2px solid  #ADD8E6 ;  /* light blue border */
        border-radius: 10px;  /* Rounded corners */
        padding: 10px 20px;  /* Padding inside the button */
        font-size: 16px;  /* Font size */
    }
    #single_result_widget{
        background-color: #252525;
        border: 2px solid black;
        border-radius: 10px;
        color: white;  
    }
    #result_widget_error{
        background-color:#DC143C;
        border: 2px solid black;
        border-radius: 10px;
        color: white;  
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
        self.json_handler = json_file()
        self.json_handler.get_list_of_file()
        self.__setup_input_grid()
        self.__setup_connection_grid()
        self.__setup_json_grid()

        self.debug_button = GUI_Factory.create_button(
            "Open Debug Window", "popup_dialog_button", GUI.main_style
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
            self.main_widget, "input_widget", GUI.main_style, 160, 825, 230
        )
        self.input_grid = QtWidgets.QGridLayout(self.input_widget)

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
            self.main_widget, "input_widget", GUI.main_style, 160, 825, 230
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

    def __setup_json_grid(self):
        # Create a new widget for the JSON grid layout
        json_widget = GUI_Factory.create_widget(
            self.main_widget, "input_widget", GUI.main_style, 160, 825, 230
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
            "Edit OS Template", "popup_dialog_button", GUI.main_style
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
        selected_file = self.json_file_dropdown.currentText()
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
        dialog = OSTemplateConfigurePage(
            self.main_widget,
            self.json_file_dropdown.currentText(),
            self.os_version_dropdown.currentText(),
        )
        dialog.exec_()

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

        command_dict_json = self.__get_command_dict(selected_os_version).copy()
        if command_dict_json is None:
            return  # User was alerted

        # Create the loading window but do not block interaction
        self._loading_window = GUI_Factory.create_loading_window(self._window_parent)

        self._loading_window.show()  # Show the loading window

        # Gather values from all QLineEdit inputs for the new thread
        connection_params = {
            "hostname": self.hostname_input.text().strip(),
            "port": self.port_input.text().strip(),
            "username": self.username_input.text().strip(),
            "password": self.password_input.text().strip(),
            "enable_password": self.enable_password_input.text().strip(),
            "connection_type": self.connection_type_button_group.checkedButton().text(),
        }

        # Create and start the new connection thread
        self.connection_thread = DataCollectorThread(
            params=connection_params,
            connection_manager=self.connection_manager,
            command_dict_json=command_dict_json,
            is_done_create_img=False,
        )
        self.connection_thread.connection_successful.connect(
            self.on_connection_successful
        )
        self.connection_thread.error_occurred.connect(self.on_error_occurred)
        self.connection_thread.data_collected.connect(self.on_data_collected)
        self.connection_thread.image_generated.connect(self.on_image_generated)
        self.connection_thread.finished.connect(self._loading_window.accept)

        self.connection_thread.start()  # Start the thread

    def on_connection_successful(self, params):
        """Handle successful connection."""
        print("Connection established successfully with parameters:", params)

        self._loading_window.update_label("Connected, Collecting data...")

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
        QtWidgets.QMessageBox.critical(
            self._window_parent, "Connection Error", error_message
        )
        self._loading_window.accept()

    def on_image_generated(self):
        self._result_page.set_result_grid()
        self._result_page.exec_()  # Show the result page

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


class DebugWindow(QtWidgets.QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("Debug Output")
        self.setGeometry(100, 100, 600, 400)  # Set size and position

        # Create a QTextEdit to display debug output
        self.text_edit = QtWidgets.QTextEdit(self)
        self.text_edit.setReadOnly(True)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.text_edit)
        self.setLayout(layout)

        # Redirect stdout to the QTextEdit
        self.original_stdout = sys.stdout  # Save the original stdout
        sys.stdout = self  # Redirect stdout to this instance

    def write(self, message):
        """Write message to the QTextEdit and ensure it auto-scrolls."""
        self.text_edit.append(message)
        # Scroll to the bottom
        self.text_edit.verticalScrollBar().setValue(
            self.text_edit.verticalScrollBar().maximum()
        )

    def flush(self):
        """Flush method for the stdout redirection."""
        pass  # No need to implement flush for QTextEdit

    def closeEvent(self, event):
        """Restore stdout when the debug window is closed."""
        sys.stdout = self.original_stdout  # Restore original stdout
        event.accept()  # Accept the close event

    def contextMenuEvent(self, event):
        """Create a context menu for the QTextEdit."""
        context_menu = QtWidgets.QMenu(self)

        clear_action = context_menu.addAction("Clear")
        action = context_menu.exec_(event.globalPos())

        if action == clear_action:
            self.text_edit.clear()  # Clear the QTextEdit content


class VariableConfigurePage:

    def __init__(self, widget_parent: QtWidgets.QMainWindow, curr_conf: dict) -> None:
        # Create a QDialog instance
        self._widget_parrent = widget_parent
        self.curr_conf = curr_conf
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
            "IP Timer Configuration",
            "label_banner",
            alignment=QtCore.Qt.AlignCenter,
            HorSizePolicy=QtWidgets.QSizePolicy.Expanding,
            VerSizePolicy=QtWidgets.QSizePolicy.Preferred,
        )

        login_wait_label = GUI_Factory.create_label(
            label_text="Login Wait Time",
            obj_name="input_label_configure_dialog",
        )
        self.login_wait_input = GUI_Factory.create_lineedit(
            obj_name="input_lineedit_configure_dialog",
            placeholder_text=f'Default {self.curr_conf["login_wait_time"]}',
        )
        self.login_wait_input.setValidator(QtGui.QDoubleValidator(self.input_widget))

        banner_timeout_label = GUI_Factory.create_label(
            label_text="Banner Timeout",
            obj_name="input_label_configure_dialog",
        )
        self.banner_timeout_input = GUI_Factory.create_lineedit(
            obj_name="input_lineedit_configure_dialog",
            placeholder_text=f'Default {self.curr_conf["banner_timeout"]}',
        )
        self.banner_timeout_input.setValidator(
            QtGui.QDoubleValidator(self.input_widget)
        )

        command_retriesdelay_label = GUI_Factory.create_label(
            label_text="Command Retries Delay",
            obj_name="input_label_configure_dialog",
        )
        self.command_retriesdelay_input = GUI_Factory.create_lineedit(
            obj_name="input_lineedit_configure_dialog",
            placeholder_text=f'Default {self.curr_conf["command_retriesdelay"]}',
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
            placeholder_text=f'Default {self.curr_conf["command_maxretries"]}',
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
            "Serial Configuration",
            "label_banner",
            alignment=QtCore.Qt.AlignCenter,
            HorSizePolicy=QtWidgets.QSizePolicy.Expanding,
            VerSizePolicy=QtWidgets.QSizePolicy.Preferred,
        )
        bytesize_label = GUI_Factory.create_label(
            label_text="Bytesize",
            obj_name="input_label_configure_dialog",
        )
        self.bytesize_input = GUI_Factory.create_lineedit(
            obj_name="input_lineedit_configure_dialog",
            placeholder_text=f'Default {self.curr_conf["bytesize"]}',
        )
        self.bytesize_input.setValidator(QtGui.QIntValidator(self.serial_widget))

        parity_label = GUI_Factory.create_label(
            label_text="Parity",
            obj_name="input_label_configure_dialog",
        )
        self.parity_input = GUI_Factory.create_lineedit(
            obj_name="input_lineedit_configure_dialog",
            placeholder_text=f'Default {self.curr_conf["parity"]}',
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
            placeholder_text=f'Default {self.curr_conf["stopbits"]}',
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


class OSTemplateConfigurePage:

    def __init__(
        self,
        widget_parent: QtWidgets.QMainWindow,
        cur_json_selected: str = "",
        cur_os_selected: str = "",
    ) -> None:
        self._widget_parent = widget_parent
        self.json_handler = json_file()  # Accepting the json_handler object
        self.OS_template_configure_page_dialog = QtWidgets.QDialog(widget_parent)
        self.OS_template_configure_page_dialog.setStyleSheet(GUI.main_style)
        self.OS_template_configure_page_dialog.setWindowTitle(
            "OS Template Configuration"
        )
        self.OS_template_configure_page_dialog.setMinimumWidth(700)
        self.OS_template_configure_page_dialog.setMinimumHeight(550)
        self.cur_json_selected = cur_json_selected
        self.cur_os_selected = cur_os_selected
        self.layout = QtWidgets.QGridLayout(self.OS_template_configure_page_dialog)

        self.__setup_comboboxes()  # Setting up the combo boxes
        self.__setup_scroll_area()  # Setting up the scroll area for command templates
        self.__setup_buttons()  # Setting up the action buttons

        # Create a container for command entries
        self.command_container = QtWidgets.QWidget()
        self.scroll_area_layout = QtWidgets.QVBoxLayout(self.command_container)
        self.scroll_area.setWidget(self.command_container)

    def __setup_comboboxes(self):
        # Label for JSON files
        json_label = GUI_Factory.create_label(
            "Select Device Configuration File:", "input_label"
        )
        json_label.setMinimumWidth(350)
        self.layout.addWidget(json_label, 0, 0)

        # ComboBox for JSON files
        self.json_file_dropdown = GUI_Factory.create_combobox(
            self._widget_parent, font_size=22
        )
        self.json_file_dropdown.setObjectName("json_dropdown")
        self.json_file_dropdown.addItems(self.json_handler.get_list_of_file())
        self.json_file_dropdown.setCurrentIndex(-1)
        self.json_file_dropdown.currentTextChanged.connect(self.on_select_new_json)
        self.layout.addWidget(self.json_file_dropdown, 0, 1)

        # Label for OS version
        os_version_label = GUI_Factory.create_label("Select OS Version:", "input_label")
        os_version_label.setMinimumWidth(350)
        self.layout.addWidget(os_version_label, 1, 0)

        # ComboBox for OS versions
        self.os_version_dropdown = GUI_Factory.create_combobox(
            self._widget_parent, font_size=22
        )
        self.os_version_dropdown.setObjectName("os_version_dropdown")
        self.layout.addWidget(self.os_version_dropdown, 1, 1)
        self.os_version_dropdown.currentTextChanged.connect(self.update_command_list)

    def __setup_scroll_area(self):
        # Create a scroll area for commands
        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        # Create a container for command entries
        self.command_container = QtWidgets.QWidget()
        self.scroll_area_layout = QtWidgets.QVBoxLayout(self.command_container)
        self.scroll_area.setWidget(self.command_container)

        # Add the scroll area to the layout
        self.layout.addWidget(self.scroll_area, 2, 0, 1, 2)  # Span across two columns

        # Initialize command list based on selected OS

    def __setup_buttons(self):
        # Button layout
        button_layout = QtWidgets.QHBoxLayout()

        # Save button
        self.save_button = GUI_Factory.create_button(
            "Save", "acceptButton", GUI.main_style
        )
        self.save_button.clicked.connect(self.save_changes)
        button_layout.addWidget(self.save_button)

        # Cancel button
        self.cancel_button = GUI_Factory.create_button(
            "Cancel", "cancelButton", GUI.main_style
        )
        self.cancel_button.clicked.connect(
            self.OS_template_configure_page_dialog.reject
        )
        button_layout.addWidget(self.cancel_button)

        self.layout.addLayout(
            button_layout, 3, 0, 1, 2
        )  # Add buttons below the scroll area

    def on_select_new_json(self):
        try:
            self.json_handler.read_json_file(self.json_file_dropdown.currentText())
            self.os_version_dropdown.clear()
            self.os_version_dropdown.addItems(self.json_handler.get_os_keys())
            self.update_command_list()
        except Exception:
            self.os_version_dropdown.clear()
            QtWidgets.QMessageBox.critical(
                self._widget_parent, "Error", "Error loading commands."
            )

    def update_command_list(self):
        """Update the list of commands based on the selected OS version."""
        self.clear_command_container()  # Remove the old container

        # Create a new command container
        self.command_container = QtWidgets.QWidget()
        self.scroll_area_layout = QtWidgets.QGridLayout(self.command_container)
        self.scroll_area.setWidget(self.command_container)

        # Retrieve selected OS version
        selected_os = self.os_version_dropdown.currentText()
        if selected_os == "":
            return

        # Load commands based on selection
        try:
            commands = self.json_handler.get_command_json(
                selected_os
            )  # Get commands from JSON

            if commands:  # Check if commands are not empty
                for index, (command_title, command_data) in enumerate(commands.items()):
                    self.__create_command_entry(command_title, command_data, index)
            else:
                # Optionally, you could display a message if there are no commands for the selected OS
                no_command_label = GUI_Factory.create_label(
                    "No commands available for this OS version.", "input_label"
                )
                self.scroll_area_layout.addWidget(no_command_label, 0, 0)

        except Error.JsonOSTemplateError:
            QtWidgets.QMessageBox.critical(
                self._widget_parent, "Error", "Error loading commands."
            )

    def clear_command_container(self):
        """Clear the old command container from the scroll area."""
        # Instead of deleting widgets, we just remove the old container and create a new one.
        self.scroll_area.setWidget(None)  # Detach the old widget
        self.command_container.deleteLater()  # Delete the old container

    def __create_command_entry(
        self, command_title: str, command_data: dict, index: int
    ):
        """Create a row for a command entry using a grid layout."""
        # Assuming self.scroll_area_layout is already a QGridLayout
        command_label = GUI_Factory.create_label(command_title, "input_label")
        command_text_edit = GUI_Factory.create_lineedit("input_lineedit")
        command_text_edit.setText(command_data["command"])  # Set initial command

        # Checkbox for activation
        active_checkbox = QtWidgets.QCheckBox("Activate")
        active_checkbox.setChecked(command_data["active"])

        # Add the widgets to the grid layout in the specified row
        self.scroll_area_layout.addWidget(
            command_label, index, 0
        )  # Column 0 for labels
        self.scroll_area_layout.addWidget(
            command_text_edit, index, 1
        )  # Column 1 for line edits
        self.scroll_area_layout.addWidget(
            active_checkbox, index, 2
        )  # Column 2 for checkboxes

    def save_changes(self):
        """Save changes to the JSON file (implement your saving logic here)."""
        os_key = (
            self.os_version_dropdown.currentText()
        )  # Get the currently selected OS version
        commands = {}  # Dictionary to hold command entries

        # Iterate through each command entry in the scroll area
        for i in range(
            self.scroll_area_layout.rowCount()
        ):  # Use rowCount to iterate through rows
            command_label_widget = self.scroll_area_layout.itemAtPosition(
                i, 0
            ).widget()  # Get command label
            command_text_edit = self.scroll_area_layout.itemAtPosition(
                i, 1
            ).widget()  # Get command line edit
            active_checkbox = self.scroll_area_layout.itemAtPosition(
                i, 2
            ).widget()  # Get the active checkbox

            if command_label_widget and command_text_edit and active_checkbox:
                command_title = (
                    command_label_widget.text()
                )  # Get command title from the label
                command_value = command_text_edit.text()  # Get command from line edit
                active_state = active_checkbox.isChecked()  # Get active state

                # Add command data to the commands dictionary
                commands[command_title] = {
                    "command": command_value,
                    "active": active_state,
                }

        # Update the os_template in the json_handler
        self.json_handler.os_template[os_key] = (
            commands  # Map the collected commands to the JSON structure
        )

        # Write the updated template back to the JSON file
        self.json_handler.write_json_file(self.json_file_dropdown.currentText())

        QtWidgets.QMessageBox.information(
            self._widget_parent, "Save", "Changes saved successfully."
        )

    def exec_(self):
        return self.OS_template_configure_page_dialog.exec_()


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


class ResultPage:
    def __init__(self, widget_parent, result: dict) -> None:
        self._widget_parent = widget_parent
        self.result_page_dialog = QtWidgets.QDialog(widget_parent)
        self.result_page_dialog.setWindowTitle("Result Viewer")
        self._result = result
        self.text_to_picture = text_to_pic()  # Instance of text_to_pic
        self.temp_image_paths = []  # To store paths of temp images
        self.main_grid = QtWidgets.QGridLayout()
        self.set_configure_grid()

    def set_result(self, result: dict):
        self._result = result

    def set_configure_grid(self):
        result_configure_widget = GUI_Factory.create_widget(
            self._widget_parent, "result_configure_widget", "", 50, 600
        )
        result_configure_grid = QtWidgets.QGridLayout(result_configure_widget)
        configure_button = GUI_Factory.create_button(
            "Result Image Configure", "popup_dialog_button"
        )
        configure_button.clicked.connect(self.show_image_configure_page)
        result_configure_grid.addWidget(configure_button, 0, 0)
        self.main_grid.addWidget(result_configure_widget, 0, 0)

    def show_image_configure_page(self):
        dialog = ResultImageConfigurePage(
            self._widget_parent, self.text_to_picture.get_cur_config()
        )

        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            user_input = dialog.get_input()
            print(user_input)
            # Set new parameters for image generation
            self.text_to_picture.set_parameters(user_input)

            # Clean up old temporary images before generating new ones
            self.cleanup_temp_images()

            # Clear the list of temp image paths after deleting old images
            self.temp_image_paths.clear()

            # Generate new images based on the updated configuration
            self.generate_all_image()

            # Rebuild the result grid with the updated temp image paths
            self.reset_result_grid()

    def reset_result_grid(self):
        """Clears the result grid and sets it up again with updated image paths."""
        # Remove the current widgets in the grid
        for i in reversed(range(self.main_grid.count())):
            widget = self.main_grid.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()  # Ensure the widget is properly deleted

        # Recreate the result grid layout with updated temp image paths
        self.set_configure_grid()
        self.set_result_grid()

    def set_result_grid(self):
        # Create the main grid layout
        # Create a widget to hold the results
        self.scroll_area = QtWidgets.QScrollArea()
        result_widget = GUI_Factory.create_widget(
            self._widget_parent, "main_window", GUI.main_style
        )
        results_layout = QtWidgets.QGridLayout(result_widget)

        # Create a scroll area
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(
            result_widget
        )  # Set the result widget as the scroll area content

        # Populate the results content with buttons for each result
        i = 0
        for title, result in self._result.items():
            if "An error occurred while executing the" in result:
                sub_widget = GUI_Factory.create_widget(
                    self._widget_parent,
                    "result_widget_error",
                    "",
                    170,
                    350,
                )
            else:
                sub_widget = GUI_Factory.create_widget(
                    self._widget_parent,
                    "single_result_widget",
                    "",
                    170,
                    350,
                )
            sub_grid = QtWidgets.QGridLayout(sub_widget)
            command_banner = GUI_Factory.create_label(
                f"{title}",
                "label_banner",
                alignment=QtCore.Qt.AlignCenter,
                HorSizePolicy=QtWidgets.QSizePolicy.Expanding,
                VerSizePolicy=QtWidgets.QSizePolicy.Preferred,
            )
            sub_grid.addWidget(command_banner, 0, 0, 1, 2)

            if "show tech-support" in title.lower():
                # If the title is "show tech-support", do not generate the image
                # Only create the Save Text button
                save_text_button = GUI_Factory.create_button(
                    f"Save {title} Text", "result_button_save_text"
                )
                save_text_button.clicked.connect(
                    lambda checked, text=result, title=title: self.save_text(
                        text, title
                    )
                )
                sub_grid.addWidget(
                    save_text_button, 1, 0, 1, 2
                )  # Span across both columns
            else:
                # Create a temporary file to hold the generated image

                # Create a button to preview the image
                preview_button = GUI_Factory.create_button(
                    f"Preview {title} Image", "result_button_preview"
                )
                preview_button.clicked.connect(
                    lambda checked, img_path=self.temp_image_paths[
                        i
                    ]: self.preview_image(img_path)
                )
                sub_grid.addWidget(preview_button, 1, 0, 1, 2)

                # Create a button to save the image
                save_image_button = GUI_Factory.create_button(
                    f"Save Image", "result_button_save_image"
                )

                save_image_button.clicked.connect(
                    lambda checked, img_path=self.temp_image_paths[
                        i
                    ], title=title: self.save_image(img_path, title)
                )
                sub_grid.addWidget(save_image_button, 2, 0)

                # Create a button to save the text
                save_text_button = GUI_Factory.create_button(
                    f"Save Text", "result_button_save_text"
                )
                save_text_button.clicked.connect(
                    lambda checked, text=result, title=title: self.save_text(
                        text, title
                    )
                )
                sub_grid.addWidget(save_text_button, 2, 1)  # Add to the right column

            results_layout.addWidget(sub_widget, i, 0)
            i += 1

        # Add the scroll area to the main grid layout

        self.main_grid.addWidget(self.scroll_area, 1, 0)

        # Set the main layout to the dialog
        self.result_page_dialog.setLayout(self.main_grid)

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

    def generate_all_image(
        self,
    ):
        for title, result in self._result.items():
            self.generate_image(result)

    def generate_image(self, text: str) -> str:
        """Generate an image from the given text and return the file path."""
        import cv2

        image = self.text_to_picture.create_text_image(text)

        # Create a temporary file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
        temp_file_path = temp_file.name

        # Save the image to the temporary file
        cv2.imwrite(temp_file_path, image)  # Save the image
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
                current_os = platform.system()  # Get the OS name
                if current_os == "Linux":
                    subprocess.Popen(["xdg-open", image_path])  # For Linux
                elif current_os == "Darwin":
                    subprocess.Popen(["open", image_path])  # For macOS
                elif current_os == "Windows":
                    subprocess.Popen(["start", image_path], shell=True)  # For Windows
                else:
                    QtWidgets.QMessageBox.warning(
                        self._widget_parent,
                        "Unsupported OS",
                        "This operating system is not supported for opening images.",
                    )
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


class ResultImageConfigurePage:

    def __init__(self, widget_parent: QtWidgets.QMainWindow, curr_conf: dict) -> None:
        self._widget_parrent = widget_parent
        self.result_image_configure_page_dialog = QtWidgets.QDialog(widget_parent)
        self.result_image_configure_page_grid_layout = QtWidgets.QGridLayout(
            self.result_image_configure_page_dialog
        )
        self.result_image_configure_page_dialog.setWindowTitle("Image Configure")

        # Initialize properties from curr_conf
        self.bg_color = curr_conf.get(
            "bg_color", (0, 0, 0)
        )  # Default to black if not set
        self.text_color = curr_conf.get(
            "text_color", (255, 255, 255)
        )  # Default to white if not set

        self.font = curr_conf.get("font", "FONT_HERSHEY_SIMPLEX")
        self.font_scale = curr_conf.get("font_scale", 1)
        self.thickness = curr_conf.get("thickness", 2)
        self.line_spacing = curr_conf.get("line_spacing", 8)
        self.padding = curr_conf.get("padding", 20)

        self.__set_image_variable_grid()
        self._set_button_grid()

    def __set_image_variable_grid(self):
        self.input_widget = GUI_Factory.create_widget(
            self._widget_parrent, "input_widget", GUI.main_style, 220, 500, 400
        )

        self.image_variable_grid = QtWidgets.QGridLayout(self.input_widget)

        # Background color label
        self.bg_color_label = GUI_Factory.create_label(
            f"BG color: {self.bg_color}",
            "",
            f"border: 2px solid black;  border-radius: 10px;  background-color: rgb{self.bg_color}; color: rgb{self.invert_color(self.bg_color)};font: 16px;",
        )
        self.bg_color_button = GUI_Factory.create_button(
            "Pick Background Color",
            "popup_dialog_button",
        )
        self.bg_color_button.clicked.connect(lambda: self.open_color_picker("bg"))

        # Text color label
        self.text_color_label = GUI_Factory.create_label(
            f"Text color: {self.text_color}",
            "",
            f"border: 2px solid black;  border-radius: 10px;  background-color: rgb{self.text_color}; color: rgb{self.invert_color(self.text_color)};font: 16px;",
        )
        self.text_color_button = GUI_Factory.create_button(
            "Pick Text Color",
            "popup_dialog_button",
        )
        self.text_color_button.clicked.connect(lambda: self.open_color_picker("text"))

        font_label = GUI_Factory.create_label(f"Font", "input_label_configure_dialog")
        self.font_dropdown = GUI_Factory.create_combobox(
            self._widget_parrent, font_size=18
        )
        self.font_dropdown.addItems(
            [
                "FONT_HERSHEY_SIMPLEX",
                "FONT_HERSHEY_PLAIN",
                "FONT_HERSHEY_DUPLEX",
                "FONT_HERSHEY_COMPLEX",
                "FONT_HERSHEY_TRIPLEX",
                "FONT_HERSHEY_COMPLEX_SMALL",
                "FONT_HERSHEY_SCRIPT_SIMPLEX",
                "FONT_HERSHEY_SCRIPT_COMPLEX",
                "FONT_ITALIC",
            ]
        )
        if self.font in [
            self.font_dropdown.itemText(i) for i in range(self.font_dropdown.count())
        ]:
            self.font_dropdown.setCurrentText(self.font)
        else:
            self.font_dropdown.setCurrentIndex(0)
        self.font_dropdown
        font_scale_label = GUI_Factory.create_label(
            "Font Scale", "input_label_configure_dialog"
        )
        self.font_scale_lineedit = GUI_Factory.create_lineedit(
            obj_name="input_lineedit_configure_dialog",
            placeholder_text=f"Default {self.font_scale}",
        )
        thickness_label = GUI_Factory.create_label(
            "Font Thickness", "input_label_configure_dialog"
        )
        self.thickness_lineedit = GUI_Factory.create_lineedit(
            obj_name="input_lineedit_configure_dialog",
            placeholder_text=f"Default {self.thickness}",
        )
        line_spacing_label = GUI_Factory.create_label(
            "Line Spacing", "input_label_configure_dialog"
        )
        self.line_spacing_lineedit = GUI_Factory.create_lineedit(
            obj_name="input_lineedit_configure_dialog",
            placeholder_text=f"Default {self.line_spacing}",
        )
        padding_label = GUI_Factory.create_label(
            "Padding", "input_label_configure_dialog"
        )
        self.padding_lineedit = GUI_Factory.create_lineedit(
            "input_lineedit_configure_dialog",
            placeholder_text=f"Default {self.padding}",
        )
        # Adding widgets to the layout
        self.image_variable_grid.addWidget(self.bg_color_label, 0, 0)
        self.image_variable_grid.addWidget(self.bg_color_button, 0, 1)
        self.image_variable_grid.addWidget(self.text_color_label, 1, 0)
        self.image_variable_grid.addWidget(self.text_color_button, 1, 1)
        self.image_variable_grid.addWidget(font_label, 2, 0)
        self.image_variable_grid.addWidget(self.font_dropdown, 2, 1)
        self.image_variable_grid.addWidget(font_scale_label, 3, 0)
        self.image_variable_grid.addWidget(self.font_scale_lineedit, 3, 1)
        self.image_variable_grid.addWidget(thickness_label, 4, 0)
        self.image_variable_grid.addWidget(self.thickness_lineedit, 4, 1)
        self.image_variable_grid.addWidget(line_spacing_label, 5, 0)
        self.image_variable_grid.addWidget(self.line_spacing_lineedit, 5, 1)
        self.image_variable_grid.addWidget(padding_label, 6, 0)
        self.image_variable_grid.addWidget(self.padding_lineedit, 6, 1)

        self.result_image_configure_page_grid_layout.addWidget(
            self.input_widget,
            0,
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
            "Cancel", "cancelButton", GUI.main_style
        )

        self.button_grid.addWidget(self.apply_button, 0, 0)
        self.button_grid.addWidget(self.cancel_button, 0, 1)
        self.apply_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

        self.result_image_configure_page_grid_layout.addWidget(self.button_widget, 2, 0)

    def open_color_picker(self, color_type):
        # Open the color picker dialog
        color = QtWidgets.QColorDialog.getColor()

        # Check if a valid color was selected
        if color.isValid():
            # Get the RGB values as a tuple of integers
            rgb_tuple = (color.red(), color.green(), color.blue())

            # Assign the selected color to the appropriate variable and update label
            if color_type == "bg":
                self.bg_color = rgb_tuple
                self.bg_color_label.setText(
                    f"BG color: {self.bg_color}"
                )  # Update label text
                self.bg_color_label.setStyleSheet(
                    f"border: 2px solid black;  border-radius: 10px;  background-color: rgb{rgb_tuple}; color: rgb{self.invert_color(rgb_tuple)}; font: 16px;"
                )
                print(f"Selected Background Color (RGB): {self.bg_color}")
            elif color_type == "text":
                self.text_color = rgb_tuple
                self.text_color_label.setText(
                    f"Text color: {self.text_color}"
                )  # Update label text
                self.text_color_label.setStyleSheet(
                    f"border: 2px solid black;  border-radius: 10px;background-color: rgb{rgb_tuple};color: rgb{self.invert_color(rgb_tuple)}; font: 16px;"
                )

                print(f"Selected Text Color (RGB): {self.text_color}")

    def invert_color(self, rgb: tuple[int, int, int]) -> tuple[int, int, int]:
        """Invert the RGB color."""
        return (255 - rgb[0], 255 - rgb[1], 255 - rgb[2])  # Invert the color

    def exec_(self):
        return self.result_image_configure_page_dialog.exec_()

    def accept(self):
        self.result = QtWidgets.QDialog.Accepted
        self.result_image_configure_page_dialog.accept()

    def reject(self):
        self.result = QtWidgets.QDialog.Rejected
        self.result_image_configure_page_dialog.reject()

    def get_input(self):
        # Fetch input values from the form elements, falling back to default values if not filled
        return {
            "bg_color": self.bg_color,
            "text_color": self.text_color,
            "font": self.font_dropdown.currentText(),
            "font_scale": (
                float(self.font_scale_lineedit.text())
                if self.font_scale_lineedit.text()
                else self.font_scale
            ),
            "thickness": (
                int(self.thickness_lineedit.text())
                if self.thickness_lineedit.text()
                else self.thickness
            ),
            "line_spacing": (
                int(self.line_spacing_lineedit.text())
                if self.line_spacing_lineedit.text()
                else self.line_spacing
            ),
            "padding": (
                int(self.padding_lineedit.text())
                if self.padding_lineedit.text()
                else self.padding
            ),
        }

    def result(self):
        return self.result


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
    def create_label(
        label_text: str,
        obj_name: str,
        stylesheet: str = "",
        alignment=None,
        HorSizePolicy=None,
        VerSizePolicy=None,
    ):
        temp_label = QtWidgets.QLabel(text=label_text)
        temp_label.setObjectName(obj_name)
        if stylesheet:
            temp_label.setStyleSheet(stylesheet)
        if alignment:
            temp_label.setAlignment(alignment)
        if HorSizePolicy is not None and VerSizePolicy is not None:
            temp_label.setSizePolicy(HorSizePolicy, VerSizePolicy)
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
    def create_radio_button(text, image_path, button_group):
        # Create a QRadioButton
        radio_button = QtWidgets.QRadioButton(text)
        # Load and set the image for the radio button
        icon = QtGui.QIcon(image_path)
        radio_button.setIcon(icon)
        radio_button.setIconSize(QtCore.QSize(24, 24))  # Set the size of the icon

        # Set the style for the radio button
        radio_button.setStyleSheet(
            """
            QRadioButton {
                background-color: #696969; 
                border-radius: 10px;
                padding: 10px;  /* Add padding to increase clickable area */
                border: none;
                color: white;
            }
            QRadioButton:hover {
                background-color: #45a049; 
                border-radius: 10px;
                padding: 10px;  /* Add padding to increase clickable area */
                border: none;
                color: white;
            }
            
            QRadioButton::checked {
                background-color: green; 
                border-radius: 10px;
                padding: 10px; 
                border: none;
                color: white;
            }
            QRadioButton::indicator {
                width: 0; /* Hide the default indicator */
                height: 0; /* Hide the default indicator */
                border: none; /* No border */
            }
            """
        )

        # Set the cursor for the radio button
        radio_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        # Add the radio button to the button group
        button_group.addButton(radio_button)

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
        width: int = 550,
        height: int = 150,
        message="Connecting to device, Please wait....",
        WindowModality=QtCore.Qt.WindowModality.NonModal,
    ):
        """Create and return an instance of the LoadingWindow class."""
        loading_window = GUI_Factory.LoadingWindow(parent, width, height, message)
        loading_window.setWindowModality(WindowModality)
        return loading_window

    @staticmethod
    def create_combobox(parent=None, font_size: int = 18):
        temp_combobox = GUI_Factory.ComboBoxWithDynamicArrow(parent, font_size)
        return temp_combobox

    def create_serial_combobox(
        connection_manager: connection_manager,
        parent=None,
        font_size: int = 18,
        width=200,
    ):
        temp_combobox = GUI_Factory.SerialPortComboBox(
            connection_manager, parent, font_size, width
        )
        return temp_combobox

    class LoadingWindow(QtWidgets.QDialog):
        def __init__(
            self,
            parent,
            width,
            height,
            message,
        ):
            super().__init__(parent)
            self.setWindowTitle("Loading")
            self.setModal(True)
            self.setFixedSize(width, height)

            self.layout = QtWidgets.QVBoxLayout(self)
            self.label = QtWidgets.QLabel(message)
            self.progress = QtWidgets.QProgressBar()
            self.progress.setRange(0, 0)  # Indeterminate progress

            self.layout.addWidget(self.label)
            self.layout.addWidget(self.progress)

        def update_label(self, new_message: str):
            """Update the label text of the loading window."""
            self.label.setText(new_message)

    class ComboBoxWithDynamicArrow(QtWidgets.QComboBox):
        def __init__(self, parent=None, fontsize=18):
            super(GUI_Factory.ComboBoxWithDynamicArrow, self).__init__(parent)

            self.combobox_style = f""" 
            QComboBox {{
                background-color: #696969; /* Dark background color */
                border: 1px solid #2F2F2F;
                border-radius: 5px;
                padding: 5px;
                color: white; 
                font-size: {str(fontsize)}px;
            }}

            QComboBox::drop-down {{
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 25px;
                border-left-width: 1px;
                border-left-color: #2F2F2F;
                border-left-style: solid;
                border-top-right-radius: 3px;
                background: #3A3A3A; /* Darker drop-down background */
                
            }}

            QComboBox QAbstractItemView {{
                border: 1px solid #2F2F2F;
                background-color: #2F2F2F; /* Darker background for the drop-down list */
                selection-background-color: #3A3A3A; /* Selection background color */
                selection-color: white; /* Selection text color */
                color: white;
                min-height: 15px;
            }}
            QComboBox::down-arrow {{
                    image: url(./src/Assets/arrow_down.png); 
                    width: 15px;
                    height: 15px;
                }}"""
            # Set the default arrow (down)
            self.setStyleSheet(self.combobox_style)

            # Connect signals for popup and close
            self.view().window().installEventFilter(self)

        def eventFilter(self, source, event):
            if event.type() == event.Show:
                self.set_arrow_up()
            elif event.type() == event.Hide:
                self.set_arrow_down()
            return super(GUI_Factory.ComboBoxWithDynamicArrow, self).eventFilter(
                source, event
            )

        def set_arrow_up(self):
            self.setStyleSheet(self.combobox_style.replace("arrow_down", "arrow_up"))

        def set_arrow_down(self):
            self.setStyleSheet(self.combobox_style)

    class SerialPortComboBox(ComboBoxWithDynamicArrow):
        def __init__(self, connection_manager, parent=None, fontsize=18, width=200):
            # Call the parent constructor (ComboBoxWithDynamicArrow)
            super().__init__(parent=parent, fontsize=fontsize)

            # Store the connection manager reference
            self.connection_manager = connection_manager
            self.setMinimumWidth(width)
            # Populate the combo box with serial ports on startup
            self.populate_serial_ports()

            # Connect the signal for when the user clicks the combo box (showing the dropdown)
            self.view().window().installEventFilter(self)

        def populate_serial_ports(self):
            """Populate the combo box with the available serial ports."""
            # Get the list of available serial ports from the connection manager
            try:
                serial_ports = self.connection_manager.get_serial_port()

                # Clear the combo box before repopulating
                self.clear()

                # Add the serial ports to the combo box
                for port in serial_ports:
                    self.addItem(port)
            except Exception:
                self.clear()
                # raise Error.NoSerialPortError()

        def eventFilter(self, source, event):
            """Event filter to handle when the combo box is clicked."""
            if event.type() == QtCore.QEvent.Show and source is self.view().window():
                # Populate the combo box with available serial ports on click
                self.populate_serial_ports()
            return super(GUI_Factory.SerialPortComboBox, self).eventFilter(
                source, event
            )
