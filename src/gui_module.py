import os
import sys
from time import sleep
from PyQt5 import QtCore, QtGui, QtWidgets


# from PyQt5.QtWidgets import *


class GUI:

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
            self.Window.setWindowTitle("Network Device Data Collection Script")
        except Exception as e:
            print(e)

    def setup_window(self):
        self.Main_Page = Main_Page(self.Window)

        self.Window.setCentralWidget(self.Main_Page.get_widget())

        self.Window.show()
        self.center_window()
        sys.exit(self.App.exec_())

    def center_window(self):
        window_geometry = self.Window.frameGeometry()

        # Get the center point of the screen
        screen_center = QtWidgets.QDesktopWidget().availableGeometry().center()

        # Move the center of the window's geometry to the screen center
        window_geometry.moveCenter(screen_center)

        # Move the top-left point of the window to the top-left of the adjusted geometry
        self.Window.move(window_geometry.topLeft())


class Main_Page:
    main_style = """
    #input_label{
        border: 2px solid black;  
        border-radius: 10px;
        padding: 5px;
        background-color: #4D4D4D;    
    }
    #enable_pass_label{
        border: 2px solid black;  
        border-radius: 10px;
        padding: 5px;
        background-color: #4D4D4D; 
        font-size: 22px;
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
    }
    """

    def __init__(self, window_parrent: QtWidgets.QMainWindow) -> None:
        self.main_widget = QtWidgets.QWidget(window_parrent)
        self.main_grid = QtWidgets.QGridLayout(self.main_widget)
        self._window_parrent = window_parrent
        self.__set_input_grid()
        self.__set_connection_grid()

    def get_widget(self):
        return self.main_widget

    def __set_input_grid(self):
        self.input_widget = QtWidgets.QWidget(self.main_widget)

        self.input_widget.setMinimumHeight(150)
        self.input_widget.setMinimumWidth(800)
        self.input_widget.setMaximumHeight(230)
        self.input_widget.setStyleSheet(
            """
            background-color: #252525;
            border: 2px solid black;
            border-radius: 10px;
            color: white;  
        """
        )
        self.input_grid = QtWidgets.QGridLayout(self.input_widget)
        self.input_grid.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        hostname_label = GUI_Factory.create_label(
            label_text="Hostname", obj_name="input_label", stylesheet=self.main_style
        )

        self.hostname_input = GUI_Factory.create_lineedit(
            obj_name="input_lineedit", stylesheet=self.main_style
        )

        port_label = GUI_Factory.create_label(
            label_text="Port", obj_name="input_label", stylesheet=self.main_style
        )

        self.port_input = GUI_Factory.create_lineedit(
            obj_name="input_lineedit", stylesheet=self.main_style
        )
        self.port_input.setValidator(QtGui.QIntValidator(self.input_widget))

        username_label = GUI_Factory.create_label(
            label_text="Username", obj_name="input_label", stylesheet=self.main_style
        )

        self.username_input = GUI_Factory.create_lineedit(
            obj_name="input_lineedit", stylesheet=self.main_style
        )

        password_label = GUI_Factory.create_label(
            label_text="Password", obj_name="input_label", stylesheet=self.main_style
        )

        self.password_input = GUI_Factory.create_lineedit(
            obj_name="input_lineedit", stylesheet=self.main_style, is_password=True
        )

        enable_password = GUI_Factory.create_label(
            label_text="Enable Password",
            obj_name="enable_pass_label",
            stylesheet=self.main_style,
        )

        self.enable_password_input = GUI_Factory.create_lineedit(
            obj_name="input_lineedit", stylesheet=self.main_style, is_password=True
        )

        self.connection_setting_button = QtWidgets.QPushButton("Connection Setting")
        self.connection_setting_button.clicked.connect(self.show_input_dialog)
        self.connection_setting_button.setStyleSheet(
            """
            QPushButton {
                background-color: #4CAF50;  /* Green background */
                color: white;  /* White text */
                border: 2px solid #4CAF50;  /* Green border */
                border-radius: 10px;  /* Rounded corners */
                padding: 10px 20px;  /* Padding inside the button */
                font-size: 16px;  /* Font size */
            }
            QPushButton:hover {
                background-color: #45a049;  /* Darker green on hover */
            }
            QPushButton:pressed {
                background-color: #388E3C;  /* Even darker green on press */
            }
        """
        )
        self.connection_setting_button.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor)
        )
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
        widget_default_style = """
            #connection_widget{
                border: 2px solid black;  
                border-radius: 10px;      
                padding: 10px;            
                background-color: #4D4D4D;
                }
            """
        self.connection_widget = QtWidgets.QWidget(self.main_widget)
        self.connection_widget.setStyleSheet(
            """
            background-color: #252525;
            border: 2px solid black;
            border-radius: 10px;
            color: white;  
        """
        )
        connection_top_widget = QtWidgets.QWidget(self.main_widget)
        connection_top_widget.setObjectName("connection_widget")
        connection_top_widget.setStyleSheet(widget_default_style)

        connection_botton_widget = QtWidgets.QWidget(self.main_widget)
        connection_botton_widget.setObjectName("connection_widget")
        connection_botton_widget.setStyleSheet(widget_default_style)

        self.connection_grid = QtWidgets.QGridLayout(self.connection_widget)
        self.connection_top_grid = QtWidgets.QGridLayout(connection_top_widget)
        self.connection_botton_grid = QtWidgets.QGridLayout(connection_botton_widget)

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

        self.connect_botton = QtWidgets.QPushButton("Connect")
        self.connect_botton.setStyleSheet(
            """
            QPushButton {
                background-color: #4CAF50; 
                color: white; 
                border: 2px solid #4CAF50; 
                border-radius: 10px; 
                padding: 10px 20px; 
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #45a049;  /* Darker green on hover */
            }
            QPushButton:pressed {
                background-color: #388E3C;  /* darker green on press */
            }
        """
        )
        self.connect_botton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        self.comport_combo_box = ComboBoxWithDynamicArrow()
        self.connection_botton_grid.addWidget(self.comport_combo_box, 0, 1)
        self.comport_combo_box.setMinimumWidth(180)

        self.connection_botton_grid.addWidget(
            GUI_Factory.create_label(
                label_text="Baudrate",
                obj_name="connection_grid_label",
                stylesheet=self.main_style,
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
        self.connection_botton_grid.addWidget(self.baudrate_combo_box, 0, 3)
        self.connection_top_grid.addWidget(ssh_button, 0, 0)
        self.connection_top_grid.addWidget(telnet_button, 0, 1)
        self.connection_top_grid.addWidget(serial_button, 0, 2)
        self.connection_top_grid.addWidget(self.connect_botton, 0, 3)
        self.connection_botton_grid.addWidget(
            GUI_Factory.create_label(
                label_text="Comport",
                obj_name="connection_grid_label",
                stylesheet=self.main_style,
            ),
            0,
            0,
        )
        self.connection_grid.addWidget(
            connection_top_widget, 0, 0, QtCore.Qt.AlignmentFlag.AlignHCenter
        )
        self.connection_grid.addWidget(
            connection_botton_widget, 1, 0, QtCore.Qt.AlignmentFlag.AlignHCenter
        )
        self.main_grid.addWidget(
            self.connection_widget,
            1,
            0,
        )

    def show_input_dialog(self):
        # Create and show the input dialog
        dialog = Variable_Configure_Page(self.main_widget)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            user_input = dialog.get_input()
            QtWidgets.QMessageBox.information(
                self.main_widget, "Input Received", f"You entered: {user_input}"
            )


class Variable_Configure_Page:
    main_style = """
    #input_label{
        border: 2px solid black;  
        border-radius: 10px;
        padding: 3px;
        background-color: #4D4D4D;    
        font: 15px;
    }
    #input_lineedit{
        border: 2px solid black;
        border-radius: 10px;
        padding: 3px;       
        min-width: 200px;
        background-color: #4D4D4D;  
    }
    #connection_grid_label{
        border: 2px solid black;  
        border-radius: 10px;
        padding: 5px;
        background-color: #696969;
    }
    """

    def __init__(self, widget_parrent: QtWidgets.QMainWindow) -> None:
        # Create a QDialog instance
        self._widget_parrent = widget_parrent
        self.dialog = QtWidgets.QDialog(widget_parrent)
        self.dialog_grid_layout = QtWidgets.QGridLayout(self.dialog)
        self.dialog.setWindowTitle("Input Dialog")
        self.dialog.setGeometry(150, 150, 300, 150)
        self._set_ip__input_variable_grid()
        # Create widgets for the dialog
        # timeout_label = GUI_Factory.create_label("Timeout", "variable_label", "")
        # self.timeout_input = GUI_Factory.create_lineedit("variable_input", "")

        # self.ok_button = QtWidgets.QPushButton("OK", self.dialog)
        # self.cancel_button = QtWidgets.QPushButton("Cancel", self.dialog)

        # Connect buttons
        # self.ok_button.clicked.connect(self.accept)
        # self.cancel_button.clicked.connect(self.reject)

    def _set_ip__input_variable_grid(self):
        self.input_widget = QtWidgets.QWidget(self._widget_parrent)

        self.input_widget.setMinimumHeight(300)
        self.input_widget.setMinimumWidth(800)
        self.input_widget.setMaximumHeight(380)
        self.input_widget.setStyleSheet(
            """
            background-color: #252525;
            border: 2px solid black;
            border-radius: 10px;
            color: white;  
            """
        )
        self.ip_variable_grid = QtWidgets.QGridLayout(self.input_widget)
        self.ip_variable_grid.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)

        login_wait_label = GUI_Factory.create_label(
            label_text="Login Wait Time",
            obj_name="input_label",
            stylesheet=self.main_style,
        )
        self.login_wait_input = GUI_Factory.create_lineedit(
            obj_name="input_lineedit", stylesheet=self.main_style
        )
        self.login_wait_input.setValidator(QtGui.QDoubleValidator(self.input_widget))

        banner_timeout_label = GUI_Factory.create_label(
            label_text="Banner Timeout",
            obj_name="input_label",
            stylesheet=self.main_style,
        )
        self.banner_timeout_input = GUI_Factory.create_lineedit(
            obj_name="input_lineedit", stylesheet=self.main_style
        )
        self.banner_timeout_input.setValidator(
            QtGui.QDoubleValidator(self.input_widget)
        )

        command_timeout_label = GUI_Factory.create_label(
            label_text="Command Timeout",
            obj_name="input_label",
            stylesheet=self.main_style,
        )
        self.command_timeout_input = GUI_Factory.create_lineedit(
            obj_name="input_lineedit", stylesheet=self.main_style
        )
        self.command_timeout_input.setValidator(
            QtGui.QDoubleValidator(self.input_widget)
        )

        bytesize_label = GUI_Factory.create_label(
            label_text="Bytesize", obj_name="input_label", stylesheet=self.main_style
        )
        self.bytesize_input = GUI_Factory.create_lineedit(
            obj_name="input_lineedit", stylesheet=self.main_style
        )
        self.bytesize_input.setValidator(QtGui.QIntValidator(self.input_widget))

        parity_label = GUI_Factory.create_label(
            label_text="Parity", obj_name="input_label", stylesheet=self.main_style
        )
        self.parity_input = GUI_Factory.create_lineedit(
            obj_name="input_lineedit", stylesheet=self.main_style
        )

        stopbits_label = GUI_Factory.create_label(
            label_text="Stopbits", obj_name="input_label", stylesheet=self.main_style
        )
        self.stopbits_input = GUI_Factory.create_lineedit(
            obj_name="input_lineedit", stylesheet=self.main_style
        )
        self.stopbits_input.setValidator(QtGui.QDoubleValidator(self.input_widget))

        # Add New Widgets to Grid
        self.ip_variable_grid.addWidget(login_wait_label, 0, 0)
        self.ip_variable_grid.addWidget(self.login_wait_input, 0, 1)
        self.ip_variable_grid.addWidget(banner_timeout_label, 0, 2)
        self.ip_variable_grid.addWidget(self.banner_timeout_input, 0, 3)
        self.ip_variable_grid.addWidget(command_timeout_label, 1, 0)
        self.ip_variable_grid.addWidget(self.command_timeout_input, 1, 1)

        self.ip_variable_grid.addWidget(bytesize_label, 2, 0)
        self.ip_variable_grid.addWidget(self.bytesize_input, 2, 1)
        self.ip_variable_grid.addWidget(parity_label, 2, 2)
        self.ip_variable_grid.addWidget(self.parity_input, 2, 3)
        self.ip_variable_grid.addWidget(stopbits_label, 3, 0)
        self.ip_variable_grid.addWidget(self.stopbits_input, 3, 1)

        self.dialog_grid_layout.addWidget(
            self.input_widget,
            0,
            0,
        )

    def exec_(self):
        return self.dialog.exec_()

    def accept(self):
        self.result = QtWidgets.QDialog.Accepted
        self.dialog.accept()

    def reject(self):
        self.result = QtWidgets.QDialog.Rejected
        self.dialog.reject()

    def get_input(self):
        return self.line_edit.text()

    def result(self):
        return self.result


class GUI_Factory:
    @staticmethod
    def create_label(label_text: str, obj_name: str, stylesheet: str):
        temp_label = QtWidgets.QLabel(text=label_text)
        temp_label.setObjectName(obj_name)
        temp_label.setStyleSheet(stylesheet)
        return temp_label

    @staticmethod
    def create_lineedit(
        obj_name: str, stylesheet: str, is_password=False, placeholder_text=""
    ):
        temp_lineedit = QtWidgets.QLineEdit()
        temp_lineedit.setObjectName(obj_name)
        temp_lineedit.setStyleSheet(stylesheet)
        if is_password:
            temp_lineedit.setEchoMode(QtWidgets.QLineEdit.Password)
        if placeholder_text:
            temp_lineedit.setPlaceholderText(placeholder_text)
        return temp_lineedit

    @staticmethod
    def create_widget(parrent: QtWidgets.QWidget, obj_name: str, stylesheet: str):
        temp_widtet = QtWidgets.QWidget(parrent)
        temp_widtet.setObjectName(obj_name)
        temp_widtet.setStyleSheet(stylesheet)

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
