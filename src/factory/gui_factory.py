from PyQt5 import QtCore, QtGui, QtWidgets
from src.communication import connection_manager


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
        terminate_callback = None,
    ):
        """Create and return an instance of the LoadingWindow class."""
        loading_window = GUI_Factory.LoadingWindow(
            parent, width, height, message, terminate_callback
        )
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
        def __init__(self, parent, width, height, message, terminate_callback):
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
            self.terminate_callback = terminate_callback  #

        def update_label(self, new_message: str):
            """Update the label text of the loading window."""
            self.label.setText(new_message)

        def closeEvent(self, event):
            """Override close event to prompt for confirmation before closing."""
            reply = QtWidgets.QMessageBox.question(
                self,
                "Confirm",
                "Do you want to terminate all connections?",
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                QtWidgets.QMessageBox.No,
            )

            if reply == QtWidgets.QMessageBox.Yes:
                if self.terminate_callback:
                    self.terminate_callback()  # Call the termination method
                event.accept()  # Allow the window to close
            else:
                event.ignore()  # Prevent closing the window

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
