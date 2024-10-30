from PyQt5 import QtCore, QtGui, QtWidgets
from src.factory.gui_factory import GUI_Factory
import src.error as Error
from src.json_handler import json_file
import json
import os


class OSTemplateConfigurePage:

    def __init__(
        self,
        widget_parent: QtWidgets.QMainWindow,
        cur_json_selected: str = "",
        cur_os_selected: str = "",
    ) -> None:
        self._widget_parent = widget_parent
        self.json_handler = json_file()
        self.OS_template_configure_page_dialog = QtWidgets.QDialog(widget_parent)
        self.OS_template_configure_page_dialog.setStyleSheet("")
        self.OS_template_configure_page_dialog.setWindowTitle(
            "OS Template Configuration"
        )
        self.OS_template_configure_page_dialog.setMinimumWidth(700)
        self.OS_template_configure_page_dialog.setMinimumHeight(550)
        self.OS_template_configure_page_dialog.setObjectName("main_bg_color")
        self.cur_json_selected = cur_json_selected
        self.cur_os_selected = cur_os_selected
        self.layout = QtWidgets.QGridLayout(self.OS_template_configure_page_dialog)

        self.__setup_comboboxes()
        self.__setup_scroll_area()
        self.__setup_buttons()

        self.command_container = GUI_Factory.create_widget(None, "input_widget")
        self.scroll_area_layout = QtWidgets.QVBoxLayout(self.command_container)
        self.scroll_area.setWidget(self.command_container)

    def __setup_comboboxes(self):

        cover_widget = GUI_Factory.create_widget(self._widget_parent, "input_widget")
        cover_widget.setStyleSheet("border: 2px solid gray; padding: 10px;")
        cover_layout = QtWidgets.QGridLayout(cover_widget)

        json_label = GUI_Factory.create_label(
            "Select Device Command File:", "input_label_configure_dialog"
        )
        json_label.setMinimumWidth(350)
        cover_layout.addWidget(json_label, 0, 0)

        self.json_file_dropdown = GUI_Factory.create_combobox(
            self._widget_parent, font_size=20
        )
        self.json_file_dropdown.setObjectName("json_dropdown")
        self.json_file_dropdown.addItems(self.json_handler.get_list_of_file())
        self.json_file_dropdown.setCurrentIndex(-1)
        self.json_file_dropdown.currentTextChanged.connect(self.on_select_new_json)
        cover_layout.addWidget(self.json_file_dropdown, 0, 1)

        os_version_label = GUI_Factory.create_label(
            "Select OS Version:", "input_label_configure_dialog"
        )
        os_version_label.setMinimumWidth(350)
        cover_layout.addWidget(os_version_label, 1, 0)

        self.os_version_dropdown = GUI_Factory.create_combobox(
            self._widget_parent, font_size=20
        )
        self.os_version_dropdown.setObjectName("os_version_dropdown")
        cover_layout.addWidget(self.os_version_dropdown, 1, 1)
        self.os_version_dropdown.currentTextChanged.connect(self.update_command_list)

        input_group_widget = self.__setup_input_group()

        self.layout.addWidget(input_group_widget, 1, 0, 1, 2)

        self.layout.addWidget(cover_widget, 0, 0, 1, 2)

    def __setup_input_group(self):
        """Create the input group layout for brand name and OS version."""
        input_group_widget = GUI_Factory.create_widget(
            self._widget_parent, "input_widget"
        )
        input_group_layout = QtWidgets.QGridLayout(input_group_widget)

        brand_name_label = GUI_Factory.create_label(
            "Brand Name:", "input_label_configure_dialog"
        )
        input_group_layout.addWidget(brand_name_label, 0, 0)

        self.brand_name_lineedit = GUI_Factory.create_lineedit(
            "input_lineedit_configure_dialog"
        )
        input_group_layout.addWidget(self.brand_name_lineedit, 0, 1)

        self.create_json_button = GUI_Factory.create_button(
            "Create JSON File", "createJsonButton", ""
        )
        self.create_json_button.clicked.connect(self.create_json_file)
        input_group_layout.addWidget(self.create_json_button, 0, 2)

        new_os_version_label = GUI_Factory.create_label(
            "New OS Version:", "input_label_configure_dialog"
        )
        input_group_layout.addWidget(new_os_version_label, 1, 0)

        self.new_os_version_lineedit = GUI_Factory.create_lineedit(
            "input_lineedit_configure_dialog"
        )
        input_group_layout.addWidget(self.new_os_version_lineedit, 1, 1)

        self.create_os_version_button = GUI_Factory.create_button(
            "Create OS Version", "createOSVersionButton", ""
        )
        self.create_os_version_button.clicked.connect(self.create_os_version)
        input_group_layout.addWidget(self.create_os_version_button, 1, 2)

        self.create_command_button = GUI_Factory.create_button(
            "Create Command", "createCommandButton", ""
        )
        self.create_command_button.clicked.connect(self.add_command)
        input_group_layout.addWidget(self.create_command_button, 2, 0, 1, 3)

        return input_group_widget

    def __setup_scroll_area(self):

        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        self.command_container = GUI_Factory.create_widget(None, "input_widget")
        self.scroll_area_layout = QtWidgets.QVBoxLayout(self.command_container)
        self.scroll_area.setWidget(self.command_container)

        self.layout.addWidget(self.scroll_area, 4, 0, 1, 2)

    def __setup_buttons(self):

        button_layout = QtWidgets.QHBoxLayout()

        self.save_button = GUI_Factory.create_button("Save", "acceptButton", "")
        self.save_button.clicked.connect(self.save_changes)
        button_layout.addWidget(self.save_button)

        self.cancel_button = GUI_Factory.create_button("Cancel", "cancelButton", "")
        self.cancel_button.clicked.connect(self.handle_cancel)
        button_layout.addWidget(self.cancel_button)
        self.layout.addLayout(button_layout, 5, 0, 1, 2)

    def on_select_new_json(self):
        try:
            if self.json_file_dropdown.currentText() == "":
                return
            self.json_handler.read_json_file(self.json_file_dropdown.currentText())
            self.os_version_dropdown.clear()
            self.os_version_dropdown.addItems(self.json_handler.get_os_keys())
            self.update_command_list()
        except Exception as e:
            self.os_version_dropdown.clear()
            print(e)
            GUI_Factory.create_critical_message_box(
                self._widget_parent, "Error", "Error loading commands."
            )

    def create_os_version(self):
        """Create a new OS version object in the JSON file."""
        new_os_version = self.new_os_version_lineedit.text().strip()

        if not new_os_version:
            GUI_Factory.create_warning_message_box(
                self._widget_parent, "Warning", "Please enter a new OS version."
            )

            return

        if new_os_version in self.json_handler.os_template:
            GUI_Factory.create_warning_message_box(
                self._widget_parent,
                "Warning",
                f"OS version '{new_os_version}' already exists.",
            )
            return

        command_structure = {}

        self.json_handler.os_template[new_os_version] = command_structure

        self.json_handler.write_json_file(self.json_file_dropdown.currentText())

        GUI_Factory.create_info_message_box(
            self._widget_parent,
            "Success",
            f"OS version '{new_os_version}' created successfully.",
        )

        self.json_handler.read_json_file(self.json_file_dropdown.currentText())

        self.os_version_dropdown.clear()
        self.os_version_dropdown.addItems(self.json_handler.get_os_keys())

        self.os_version_dropdown.setCurrentText(new_os_version)

        self.new_os_version_lineedit.clear()

    def handle_cancel(self):
        """Handle the cancel button click to discard changes and update command list."""

        selected_json = self.json_file_dropdown.currentText()
        if selected_json:

            self.json_handler.read_json_file(selected_json)
            self.update_command_list()
        else:

            self.OS_template_configure_page_dialog.reject()

    def update_command_list(self):
        """Update the list of commands based on the selected OS version."""
        self.clear_command_container()

        self.command_container = GUI_Factory.create_widget(None, "input_widget")

        self.scroll_area_layout = QtWidgets.QGridLayout(self.command_container)
        self.scroll_area.setWidget(self.command_container)

        selected_os = self.os_version_dropdown.currentText()
        if selected_os == "":
            return

        try:
            commands = self.json_handler.get_command_json(selected_os)

            if commands:
                for index, (command_title, command_data) in enumerate(commands.items()):
                    self.__create_command_entry(command_title, command_data, index)
                self.no_command_label = None
            else:

                self.no_command_label = GUI_Factory.create_label(
                    "No commands available for this OS version.", "input_label"
                )
                self.scroll_area_layout.addWidget(self.no_command_label)

        except Error.JsonOSTemplateError as e:
            print(e)
            GUI_Factory.create_critical_message_box(
                self._widget_parent, "Error", "Error loading commands."
            )

    def clear_command_container(self):
        """Clear the old command container from the scroll area."""

        self.scroll_area.setWidget(None)
        if self.command_container:
            self.command_container.deleteLater()

        self.command_container = GUI_Factory.create_widget(None, "input_widget")
        self.scroll_area_layout = QtWidgets.QGridLayout(self.command_container)
        self.scroll_area.setWidget(self.command_container)

    def __create_command_entry(
        self, command_title: str, command_data: dict, index: int
    ):
        """Create a row for a command entry using a grid layout."""
        command_label = GUI_Factory.create_label(
            command_title, "input_label_configure_dialog"
        )
        command_text_edit = GUI_Factory.create_lineedit(
            "input_lineedit_configure_dialog"
        )
        command_text_edit.setText(command_data["command"])

        active_checkbox = QtWidgets.QCheckBox("Activate")
        active_checkbox.setObjectName("activeCheckbox")
        active_checkbox.setChecked(command_data["active"])

        delete_button = GUI_Factory.create_button("Delete", "deleteButton")
        delete_button.clicked.connect(lambda: self.delete_command_entry(index))

        self.scroll_area_layout.addWidget(command_label, index, 0)
        self.scroll_area_layout.addWidget(command_text_edit, index, 1)
        self.scroll_area_layout.addWidget(active_checkbox, index, 2)
        self.scroll_area_layout.addWidget(delete_button, index, 3)

    def update_json_file_dropdown(self):
        """Update the JSON file dropdown with the latest file list."""
        self.json_handler.get_list_of_file()

        if self.json_handler.file_list:
            self.json_file_dropdown.clear()
            self.json_file_dropdown.addItems(sorted(self.json_handler.file_list))
        else:
            GUI_Factory.create_warning_message_box(
                self._widget_parent,
                "Warning",
                "No JSON files available in the directory.",
            )

    def create_json_file(self):
        """Create a JSON file with the brand name and include the OS version as an object."""
        brand_name = self.brand_name_lineedit.text().strip()
        os_version = self.new_os_version_lineedit.text().strip()

        if not brand_name or not os_version:
            GUI_Factory.create_warning_message_box(
                self._widget_parent,
                "Warning",
                "Please enter both brand name and OS version.",
            )
            return

        file_path = os.path.join("command_template", f"{brand_name}.json")

        if os.path.exists(file_path):
            GUI_Factory.create_warning_message_box(
                self._widget_parent, "Warning", "File already exists."
            )
            return

        json_content = {os_version: {}}

        with open(file_path, "w") as json_file:
            json.dump(json_content, json_file, indent=4)
        GUI_Factory.create_info_message_box(
            self._widget_parent,
            "Success",
            f"JSON file '{brand_name}.json' created successfully.",
        )

        self.update_json_file_dropdown()

        self.json_file_dropdown.setCurrentText(brand_name + ".json")

        self.json_handler.read_json_file(self.json_file_dropdown.currentText())
        self.os_version_dropdown.clear()
        self.os_version_dropdown.addItems(self.json_handler.get_os_keys())
        self.os_version_dropdown.setCurrentText(os_version)

    def add_command(self):
        """Add a command to the current OS template based on the command title."""
        os_key = self.os_version_dropdown.currentText()
        if os_key == "":
            GUI_Factory.create_warning_message_box(
                self._widget_parent, "Warning", "Please select an OS version first."
            )
            return

        command_title, ok = QtWidgets.QInputDialog.getText(
            self._widget_parent, "Command Title", "Enter Command Title:"
        )
        if not ok or not command_title:
            return

        command_data = {
            "command": "",
            "active": True,
        }

        if hasattr(self, "no_command_label") and self.no_command_label is not None:
            self.no_command_label.deleteLater()
            self.no_command_label = None

        row_count = self.scroll_area_layout.count()

        self.__create_command_entry(command_title, command_data, row_count)
        GUI_Factory.create_info_message_box(
            self._widget_parent,
            "Success",
            f"Command '{command_title}' added successfully.",
        )

    def delete_command_entry(self, index: int):
        """Delete the command entry at the specified index."""

        start_position = index * 4

        for i in range(4):
            item = self.scroll_area_layout.itemAt(start_position)
            if item is not None:
                widget = item.widget()
                if widget:
                    widget.deleteLater()
                self.scroll_area_layout.removeItem(item)

    def save_changes(self):
        """Save changes to the JSON file."""
        os_key = self.os_version_dropdown.currentText()
        if os_key == "":
            GUI_Factory.create_warning_message_box(
                self._widget_parent, "Warning", "Please select an OS version first."
            )
            return

        commands = {}

        for i in range(self.scroll_area_layout.count() // 4):
            command_label_widget = self.scroll_area_layout.itemAt(i * 4).widget()
            command_text_edit = self.scroll_area_layout.itemAt(i * 4 + 1).widget()
            active_checkbox = self.scroll_area_layout.itemAt(i * 4 + 2).widget()

            if command_label_widget and command_text_edit and active_checkbox:
                command_title = command_label_widget.text()
                command_value = command_text_edit.text()
                active_state = active_checkbox.isChecked()

                commands[command_title] = {
                    "command": command_value,
                    "active": active_state,
                }

        self.json_handler.os_template[os_key] = commands

        self.json_handler.write_json_file(self.json_file_dropdown.currentText())
        GUI_Factory.create_info_message_box(
            self._widget_parent, "Save", "Changes saved successfully."
        )
        self.update_command_list()

    def exec_(self):
        return self.OS_template_configure_page_dialog.exec_()
