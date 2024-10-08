from PyQt5 import QtCore, QtGui, QtWidgets
from src.factory.gui_factory import GUI_Factory
import src.error as Error

from src.json_handler import json_file


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
        self.OS_template_configure_page_dialog.setStyleSheet("")
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
        self.save_button = GUI_Factory.create_button("Save", "acceptButton", "")
        self.save_button.clicked.connect(self.save_changes)
        button_layout.addWidget(self.save_button)

        # Cancel button
        self.cancel_button = GUI_Factory.create_button("Cancel", "cancelButton", "")
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
