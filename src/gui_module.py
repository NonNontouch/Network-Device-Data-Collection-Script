import os
import sys
from time import sleep
from PyQt5 import QtCore, QtGui, QtWidgets


# from PyQt5.QtWidgets import *


class GUI:
    main_style = """
    #main_window{
        background-color: #1C1C1C;
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
    }
    #connection_grid_label{
        border: 2px solid black;  
        border-radius: 10px;
        padding: 5px;
        background-color: #696969;
        color: white;
    }
    #sub_connection_widget{
        background-color: #4D4D4D;
        border-radius: 10px;      
        border: 2px solid black;  
        padding: 10px;            
    }
    #connection_widget{
        background-color: #252525;
        border: 2px solid black;
        border-radius: 10px;
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
    #configure_dialog_banner{
       font-size: 18px; 
        font-weight: bold; 
        color: white; 
        padding: 10px; 
        background-color: #4D4D4D;
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
            self.Window.setStyleSheet(GUI.main_style)
            self.Window.setWindowTitle("Network Device Data Collection Script")
        except Exception as e:
            print(e)

    def setup_window(self):
        self.Main_Page = Main_Page(self.Window)

        self.Window.setCentralWidget(self.Main_Page.get_widget())

        self.Window.show()
        GUI_Factory.center_window(self.Window)
        sys.exit(self.App.exec_())


class Main_Page:

    def __init__(self, window_parrent: QtWidgets.QMainWindow) -> None:
        self.main_widget = QtWidgets.QWidget(window_parrent)
        self.main_grid = QtWidgets.QGridLayout(self.main_widget)
        self._window_parrent = window_parrent
        self.__set_input_grid()
        self.__set_connection_grid()
        self.__set_json_grid()

    def get_widget(self):
        return self.main_widget

    def __set_input_grid(self):
        self.input_widget = GUI_Factory.create_widget(
            self.main_widget, "input_widget", GUI.main_style
        )
        self.input_widget.setMinimumHeight(150)
        self.input_widget.setMinimumWidth(800)
        self.input_widget.setMaximumHeight(230)

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

        self.connection_setting_button = GUI_Factory.create_button(
            "Connection Setting", "popup_dialog_button", GUI.main_style
        )
        self.connection_setting_button.clicked.connect(self.show_input_dialog)
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
            self.connection_setting_button,
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

    def __set_connection_grid(self):
        self.connection_widget = GUI_Factory.create_widget(
            self.main_widget, "connection_widget", GUI.main_style
        )

        connection_top_widget = GUI_Factory.create_widget(
            self.main_widget, "sub_connection_widget", GUI.main_style
        )

        connection_botton_widget = GUI_Factory.create_widget(
            self.main_widget, "sub_connection_widget", GUI.main_style
        )

        connection_grid = QtWidgets.QGridLayout(self.connection_widget)
        connection_top_grid = QtWidgets.QGridLayout(connection_top_widget)
        connection_botton_grid = QtWidgets.QGridLayout(connection_botton_widget)

        self.connection_type_button_group = QtWidgets.QButtonGroup(self.main_widget)
        ssh_button = GUI_Factory.create_radio_button(
            "SSH", "./src/Assets/SSH.png", self.connection_type_button_group
        )
        ssh_button.setChecked(True)

        telnet_button = GUI_Factory.create_radio_button(
            "Telnet", "./src/Assets/Telnet.png", self.connection_type_button_group
        )

        serial_button = GUI_Factory.create_radio_button(
            "Serial", "./src/Assets/RS232.png", self.connection_type_button_group
        )

        self.connect_botton = GUI_Factory.create_button(
            "Connect", "popup_dialog_button", GUI.main_style
        )

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

    def __set_json_grid(self):
        json_edit_button = GUI_Factory.create_button(
            "Edit Template", "popup_dialog_button", GUI.main_style
        )
        self.main_grid.addWidget(json_edit_button, 2, 0)
        pass

    def show_input_dialog(self):
        # Create and show the input dialog
        dialog = Variable_Configure_Page(self.main_widget)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            user_input = dialog.get_input()
            print(user_input)


class Variable_Configure_Page:

    def __init__(self, widget_parrent: QtWidgets.QMainWindow) -> None:
        # Create a QDialog instance
        self._widget_parrent = widget_parrent
        self.dialog = QtWidgets.QDialog(widget_parrent)
        self.dialog_grid_layout = QtWidgets.QGridLayout(self.dialog)
        self.dialog.setWindowTitle("Input Dialog")
        self._set_ip_input_variable_grid()
        self._set_serial_input_grid()
        self._set_button_grid()

    def _set_ip_input_variable_grid(self):
        self.input_widget = GUI_Factory.create_widget(
            self._widget_parrent, "input_widget", GUI.main_style
        )

        self.input_widget.setMinimumHeight(220)
        self.input_widget.setMinimumWidth(500)
        self.input_widget.setMaximumHeight(400)
        self.ip_variable_grid = QtWidgets.QGridLayout(self.input_widget)
        self.ip_variable_grid.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)

        banner_label = GUI_Factory.create_label(
            "IP Timer Configuration", "configure_dialog_banner", GUI.main_style
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
        self.dialog_grid_layout.addWidget(
            self.input_widget,
            0,
            0,
        )

    def _set_serial_input_grid(self):
        self.serial_widget = GUI_Factory.create_widget(self._widget_parrent,"input_widget")
        
        self.serial_widget.setMinimumHeight(180)
        self.serial_widget.setMinimumWidth(500)
        self.serial_widget.setMaximumHeight(400)
      
        self.serial_variable_grid = QtWidgets.QGridLayout(self.serial_widget)
        banner_label = GUI_Factory.create_label(
            "Serial Configuration", "configure_dialog_banner", GUI.main_style
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
        self.dialog_grid_layout.addWidget(
            self.serial_widget,
            1,
            0,
        )

    def _set_button_grid(self):
        self.button_widget = QtWidgets.QWidget(self._widget_parrent)
        self.button_widget.setMinimumHeight(40)
        self.button_widget.setMinimumWidth(500)
        self.button_widget.setMaximumHeight(100)
        self.button_widget.setStyleSheet(
            """
            background-color: #252525;
            border: 2px solid black;
            border-radius: 10px;
            color: white;  
            """
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

        self.dialog_grid_layout.addWidget(self.button_widget, 2, 0)

    def exec_(self):
        return self.dialog.exec_()

    def accept(self):
        self.result = QtWidgets.QDialog.Accepted
        self.dialog.accept()

    def reject(self):
        self.result = QtWidgets.QDialog.Rejected
        self.dialog.reject()

    def get_input(self):
        return {
            "login_wait_time": self.login_wait_input.text(),
            "banner_timeout": self.banner_timeout_input.text(),
            "command_timeout": self.command_retriesdelay_input.text(),
            "command_max_retries": self.command_maxretries_input.text(),
            "bytesize": self.bytesize_input.text(),
            "parity": self.parity_input.text(),
            "stopbits": self.stopbits_input.text(),
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
    def create_widget(parrent: QtWidgets.QWidget, obj_name: str, stylesheet: str = ""):
        temp_widtet = QtWidgets.QWidget(parrent)
        temp_widtet.setObjectName(obj_name)
        if stylesheet:
            temp_widtet.setStyleSheet(stylesheet)
        return temp_widtet

    @staticmethod
    def create_button(text: str, obj_name: str, stylesheet: str = ""):
        temp_button = QtWidgets.QPushButton(text)
        temp_button.setObjectName(obj_name)
        temp_button.setStyleSheet(stylesheet)
        temp_button.setCursor(QtCore.Qt.PointingHandCursor)
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
