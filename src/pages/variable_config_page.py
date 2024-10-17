from PyQt5 import QtCore, QtGui, QtWidgets
from src.factory.gui_factory import GUI_Factory


class VariableConfigurePage:

    def __init__(self, widget_parent: QtWidgets.QMainWindow, curr_conf: dict) -> None:
        # Create a QDialog instance
        self._widget_parrent = widget_parent
        self.curr_conf = curr_conf
        self.varialbe_configure_page_dialog = QtWidgets.QDialog(widget_parent)
        self.varialbe_configure_page_dialog.setObjectName("main_bg_color")
        self.verialbe_configure_page_grid_layout = QtWidgets.QGridLayout(
            self.varialbe_configure_page_dialog
        )
        self.varialbe_configure_page_dialog.setWindowTitle("Edit Connection Variable")
        self.__set_ip_input_variable_grid()
        self.__set_serial_input_grid()
        self._set_button_grid()

    def __set_ip_input_variable_grid(self):
        self.input_widget = GUI_Factory.create_widget(
            self._widget_parrent, "input_widget", "", 220, 500, 400
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
            self._widget_parrent, "input_widget", "", 180, 500, 400
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
            self._widget_parrent, "input_widget", "", 40, 500, 100
        )

        self.button_grid = QtWidgets.QGridLayout(self.button_widget)

        self.apply_button = GUI_Factory.create_button("Apply", "acceptButton", "")
        self.cancel_button = GUI_Factory.create_button("Cancel", "cancelButton", "")

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
