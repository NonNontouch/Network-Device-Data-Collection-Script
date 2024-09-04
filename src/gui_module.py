import sys
from time import sleep
from PyQt5 import QtCore, QtGui, QtWidgets


# from PyQt5.QtWidgets import *


class GUI:
    default_text_font = QtGui.QFont("BAHNSCHRIFT.TTF", 18)

    def __init__(self) -> None:
        self.App = QtWidgets.QApplication(sys.argv)
        self.App.setFont(self.default_text_font)
        self.Window = QtWidgets.QMainWindow()
        self.central_widget = QtWidgets.QWidget(self.Window)
        self.QDialog = QtWidgets.QDialog(self.Window)

    def set_input_grid(self):
        qlabel_style = """
        QLabel {
                border: 2px solid black;  /* 2px thick solid black border */
                border-radius: 10px;      /* Rounded corners with a 15px radius */
                padding: 5px;            /* Optional: Adds padding inside the border */
                background-color: #333333;    
            }
        """
        qlineedit_style = """
            QLineEdit {
                border: 2px solid black;   /* 2px thick solid black border */
                border-radius: 10px;       /* Optional: Rounded corners */
                padding: 5px;              /* Space inside the QLineEdit, between text and border */
                background-color: #333333;  
            }
        """
        self.input_widget = QtWidgets.QWidget(self.central_widget)
        self.input_widget.setFixedHeight(180)
        self.input_widget.setStyleSheet(
            """
            background-color: #252525;
            border: 2px solid black;
        """
        )
        self.input_grid = QtWidgets.QGridLayout(self.input_widget)
        self.input_grid.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        hostname_label = QtWidgets.QLabel(text="Hostname")
        hostname_label.setStyleSheet(qlabel_style)
        self.input_grid.addWidget(hostname_label, 0, 0)
        self.hostname_input = QtWidgets.QLineEdit(self.Window)
        self.hostname_input.setStyleSheet(qlineedit_style)
        self.input_grid.addWidget(self.hostname_input, 0, 1)

        port_label = QtWidgets.QLabel(text="Port")
        port_label.setStyleSheet(qlabel_style)
        self.input_grid.addWidget(port_label, 0, 2)
        self.port_input = QtWidgets.QLineEdit(self.Window)
        self.port_input.setStyleSheet(qlineedit_style)
        self.port_input.setValidator(QtGui.QIntValidator(self.input_widget))
        self.input_grid.addWidget(self.port_input, 0, 3)

        username_label = QtWidgets.QLabel(text="Username")
        username_label.setStyleSheet(qlabel_style)
        self.input_grid.addWidget(username_label, 1, 0)
        self.username_input = QtWidgets.QLineEdit(self.Window)
        self.username_input.setStyleSheet(qlineedit_style)
        self.input_grid.addWidget(self.username_input, 1, 1)

        password_label = QtWidgets.QLabel(text="Password")
        password_label.setStyleSheet(qlabel_style)
        self.input_grid.addWidget(password_label, 1, 2)
        self.password_input = QtWidgets.QLineEdit(self.Window)
        self.password_input.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password_input.setStyleSheet(qlineedit_style)
        self.input_grid.addWidget(self.password_input, 1, 3)

        enable_password = QtWidgets.QLabel(text="Enable\nPassword")
        enable_password.setStyleSheet(qlabel_style)
        self.input_grid.addWidget(enable_password, 2, 0)
        self.enable_password_input = QtWidgets.QLineEdit(self.Window)
        self.enable_password_input.setEchoMode(QtWidgets.QLineEdit.Password)
        self.enable_password_input.setStyleSheet(qlineedit_style)
        self.input_grid.addWidget(self.enable_password_input, 2, 1)

        self.connection_setting = QtWidgets.QPushButton("Connection Setting")
        self.connection_setting.setStyleSheet(
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
        self.connection_setting.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.input_grid.addWidget(
            self.connection_setting,
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

    def set_connection_grid(self):
        self.connection_widget = QtWidgets.QWidget(self.central_widget)

        self.connection_grid = QtWidgets.QGridLayout(self.connection_widget)

        self.connection_type_button_group = QtWidgets.QButtonGroup(self.Window)
        ssh_button = self.create_radio_button("SSH", "./src/Assets/SSH.png")
        ssh_button.setChecked(True)
        ssh_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.connection_grid.addWidget(ssh_button, 0, 0)

        telnet_button = self.create_radio_button("Telnet", "./src/Assets/Telnet.png")
        telnet_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.connection_grid.addWidget(telnet_button, 0, 1)

        serial_button = self.create_radio_button("Serial", "./src/Assets/RS232.png")
        serial_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.connection_grid.addWidget(serial_button, 0, 2)

        self.connection_grid.addWidget(QtWidgets.QLabel(text="Comport"), 0, 3)
        self.comport_combo_box = QtWidgets.QComboBox()
        self.connection_grid.addWidget(self.comport_combo_box, 0, 4)

        self.connection_grid.addWidget(QtWidgets.QLabel(text="Baudrate"), 0, 5)
        self.baudrate_combo_box = QtWidgets.QComboBox()
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
        self.connection_grid.addWidget(self.baudrate_combo_box, 0, 6)

        self.main_grid.addWidget(
            self.connection_widget,
            1,
            0,
        )
        return

    def create_radio_button(self, text, image_path):
        # Create a QRadioButton
        radio_button = QtWidgets.QRadioButton(text)

        # Load and set the image for the radio button
        icon = QtGui.QIcon(image_path)
        radio_button.setIcon(icon)
        radio_button.setIconSize(QtCore.QSize(16, 16))  # Set the size of the icon
        radio_button.setStyleSheet(
            """
            QRadioButton::indicator {
                width: 24px;
                height: 24px;
                border: 2px solid black;
                background-color: white;  /* White background for unchecked state */
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

        # Add the radio button to the button group
        self.connection_type_button_group.addButton(radio_button)
        return radio_button

    def setup_window(self):
        self.main_grid = QtWidgets.QGridLayout(self.central_widget)
        self.Window.setCentralWidget(self.central_widget)
        self.Window.setFixedHeight(800)
        self.Window.setFixedWidth(800)

        self.Window.setWindowTitle("PyQt5")
        self.set_input_grid()
        self.set_connection_grid()
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
