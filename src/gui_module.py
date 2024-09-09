import os
import sys
from time import sleep
from PyQt5 import QtCore, QtGui, QtWidgets


# from PyQt5.QtWidgets import *


class GUI:
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
                border: 2px solid black;   /* 2px thick solid black border */
                border-radius: 10px;       /* Optional: Rounded corners */
                padding: 5px;              /* Space inside the QLineEdit, between text and border */
                min-width: 200px;
                background-color: #4D4D4D;  
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
            self.central_widget = QtWidgets.QWidget(self.Window)
            self.QDialog = QtWidgets.QDialog(self.Window)
        except Exception as e:
            print(e)

    def set_input_grid(self):
        self.input_widget = QtWidgets.QWidget(self.central_widget)

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
        self.input_grid.addWidget(hostname_label, 0, 0)
        self.hostname_input = GUI_Factory.create_lineedit(
            obj_name="input_lineedit", stylesheet=self.main_style
        )
        self.input_grid.addWidget(self.hostname_input, 0, 1)

        port_label = GUI_Factory.create_label(
            label_text="Port", obj_name="input_label", stylesheet=self.main_style
        )
        self.input_grid.addWidget(port_label, 0, 2)
        self.port_input = GUI_Factory.create_lineedit(
            obj_name="input_lineedit", stylesheet=self.main_style
        )
        self.port_input.setValidator(QtGui.QIntValidator(self.input_widget))
        self.input_grid.addWidget(self.port_input, 0, 3)

        username_label = GUI_Factory.create_label(
            label_text="Username", obj_name="input_label", stylesheet=self.main_style
        )
        self.input_grid.addWidget(username_label, 1, 0)
        self.username_input = GUI_Factory.create_lineedit(
            obj_name="input_lineedit", stylesheet=self.main_style
        )
        self.input_grid.addWidget(self.username_input, 1, 1)

        password_label = GUI_Factory.create_label(
            label_text="Password", obj_name="input_label", stylesheet=self.main_style
        )
        self.input_grid.addWidget(password_label, 1, 2)
        self.password_input = GUI_Factory.create_lineedit(
            obj_name="input_lineedit", stylesheet=self.main_style, is_password=True
        )
        self.input_grid.addWidget(self.password_input, 1, 3)

        enable_password = GUI_Factory.create_label(
            label_text="Enable Password",
            obj_name="enable_pass_label",
            stylesheet=self.main_style,
        )

        self.input_grid.addWidget(enable_password, 2, 0)
        self.enable_password_input = GUI_Factory.create_lineedit(
            obj_name="input_lineedit", stylesheet=self.main_style, is_password=True
        )
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
        widget_default_style = """
            #connection_widget{
                border: 2px solid black;  
                border-radius: 10px;      
                padding: 10px;            
                background-color: #4D4D4D;
                }
            """
        self.connection_widget = QtWidgets.QWidget(self.central_widget)
        self.connection_widget.setStyleSheet(
            """
            background-color: #252525;
            border: 2px solid black;
            border-radius: 10px;
            color: white;  
        """
        )
        connection_top_widget = QtWidgets.QWidget(self.central_widget)
        connection_top_widget.setObjectName("connection_widget")
        connection_top_widget.setStyleSheet(widget_default_style)

        connection_botton_widget = QtWidgets.QWidget(self.central_widget)
        connection_botton_widget.setObjectName("connection_widget")
        connection_botton_widget.setStyleSheet(widget_default_style)

        self.connection_grid = QtWidgets.QGridLayout(self.connection_widget)
        self.connection_top_grid = QtWidgets.QGridLayout(connection_top_widget)
        self.connection_botton_grid = QtWidgets.QGridLayout(connection_botton_widget)

        self.connection_type_button_group = QtWidgets.QButtonGroup(self.Window)
        ssh_button = self.create_radio_button("SSH", "./src/Assets/SSH.png")
        ssh_button.setChecked(True)
        ssh_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.connection_top_grid.addWidget(ssh_button, 0, 0)

        telnet_button = self.create_radio_button("Telnet", "./src/Assets/Telnet.png")
        telnet_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.connection_top_grid.addWidget(telnet_button, 0, 1)

        serial_button = self.create_radio_button("Serial", "./src/Assets/RS232.png")
        serial_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.connection_top_grid.addWidget(serial_button, 0, 2)

        self.connect_botton = QtWidgets.QPushButton("Connect")
        self.connect_botton.setStyleSheet(
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
        self.connect_botton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.connection_top_grid.addWidget(self.connect_botton, 0, 3)

        self.connection_botton_grid.addWidget(
            GUI_Factory.create_label(
                label_text="Comport", obj_name="input_label", stylesheet=self.main_style
            ),
            0,
            0,
        )
        self.comport_combo_box = ComboBoxWithDynamicArrow()
        self.connection_botton_grid.addWidget(self.comport_combo_box, 0, 1)
        self.comport_combo_box.setMinimumWidth(180)

        self.connection_botton_grid.addWidget(
            GUI_Factory.create_label(
                label_text="Baudrate",
                obj_name="input_label",
                stylesheet=self.main_style,
            ),
            0,
            2,
        )
        self.baudrate_combo_box = ComboBoxWithDynamicArrow()
        self.baudrate_combo_box.setMinimumWidth(100)

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
                width: 16px;
                height: 16px;
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


class ComboBoxWithDynamicArrow(QtWidgets.QComboBox):
    def __init__(self, parent=None):
        super(ComboBoxWithDynamicArrow, self).__init__(parent)
        self.combobox_style = """ 
        QComboBox {
            background-color: #4D4D4D; /* Dark background color */
            border: 1px solid #2F2F2F;
            border-radius: 5px;
            padding: 5px;
            color: white; 
            font-size: 16px; /* Font size for text inside the QComboBox */
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


class GUI_Factory:
    @staticmethod
    def create_label(label_text: str, obj_name: str, stylesheet: str):
        temp_label = QtWidgets.QLabel(text=label_text)
        temp_label.setObjectName(obj_name)
        temp_label.setStyleSheet(stylesheet)
        return temp_label

    @staticmethod
    def create_lineedit(obj_name: str, stylesheet: str, is_password=False):
        temp_lineedit = QtWidgets.QLineEdit()
        temp_lineedit.setObjectName(obj_name)
        temp_lineedit.setStyleSheet(stylesheet)
        if is_password:
            temp_lineedit.setEchoMode(QtWidgets.QLineEdit.Password)
        return temp_lineedit

    @staticmethod
    def create_widget(parrent: QtWidgets.QWidget, obj_name: str, stylesheet: str):
        temp_widtet = QtWidgets.QWidget(parrent)
        temp_widtet.setObjectName(obj_name)
        temp_widtet.setStyleSheet(stylesheet)
