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
        self.json_handler = json_file()  # Accepting the json_handler object
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

        self.__setup_comboboxes()  # Setting up the combo boxes
        self.__setup_scroll_area()  # Setting up the scroll area for command templates
        self.__setup_buttons()  # Setting up the action buttons

        # Create a container for command entries
        self.command_container = QtWidgets.QWidget()
        self.scroll_area_layout = QtWidgets.QVBoxLayout(self.command_container)
        self.scroll_area.setWidget(self.command_container)

    def __setup_comboboxes(self):
        # Create the cover widget as a QWidget to act as a border
        cover_widget = GUI_Factory.create_widget(
            self._widget_parent, "input_widget"
        )  # Use GUI_Factory to create a widget
        cover_widget.setStyleSheet(
            "border: 2px solid gray; padding: 10px;"
        )  # Define border style
        cover_layout = QtWidgets.QGridLayout(
            cover_widget
        )  # Grid layout for cover widget

        # Label for JSON files
        json_label = GUI_Factory.create_label(
            "Select Device Configuration File:", "input_label_configure_dialog"
        )
        json_label.setMinimumWidth(350)
        cover_layout.addWidget(json_label, 0, 0)  # Add to grid layout

        # ComboBox for JSON files
        self.json_file_dropdown = GUI_Factory.create_combobox(
            self._widget_parent, font_size=20
        )
        self.json_file_dropdown.setObjectName("json_dropdown")
        self.json_file_dropdown.addItems(self.json_handler.get_list_of_file())
        self.json_file_dropdown.setCurrentIndex(-1)
        self.json_file_dropdown.currentTextChanged.connect(self.on_select_new_json)
        cover_layout.addWidget(self.json_file_dropdown, 0, 1)  # Add to grid layout

        # Label for OS version
        os_version_label = GUI_Factory.create_label(
            "Select OS Version:", "input_label_configure_dialog"
        )
        os_version_label.setMinimumWidth(350)
        cover_layout.addWidget(os_version_label, 1, 0)  # Add to grid layout

        # ComboBox for OS versions
        self.os_version_dropdown = GUI_Factory.create_combobox(
            self._widget_parent, font_size=20
        )
        self.os_version_dropdown.setObjectName("os_version_dropdown")
        cover_layout.addWidget(self.os_version_dropdown, 1, 1)  # Add to grid layout
        self.os_version_dropdown.currentTextChanged.connect(self.update_command_list)

        # Create a separate widget for the input group layout
        input_group_widget = self.__setup_input_group()

        # Add the input group widget to the main layout
        self.layout.addWidget(
            input_group_widget, 1, 0, 1, 2
        )  # Adjust position as needed

        # Finally, add the cover widget to the main layout
        self.layout.addWidget(cover_widget, 0, 0, 1, 2)  # Span across two columns

    def __setup_input_group(self):
        """Create the input group layout for brand name and OS version."""
        input_group_widget = GUI_Factory.create_widget(
            self._widget_parent, "input_widget"
        )
        input_group_layout = QtWidgets.QGridLayout(
            input_group_widget
        )  # Grid layout for input group

        # Label for Brand Name
        brand_name_label = GUI_Factory.create_label(
            "Brand Name:", "input_label_configure_dialog"
        )
        input_group_layout.addWidget(
            brand_name_label, 0, 0
        )  # Row 0, Column 0 for the label

        # LineEdit for brand name input
        self.brand_name_lineedit = GUI_Factory.create_lineedit(
            "input_lineedit_configure_dialog"
        )
        input_group_layout.addWidget(
            self.brand_name_lineedit, 0, 1
        )  # Row 0, Column 1 for the line edit

        # Create JSON File Button
        self.create_json_button = GUI_Factory.create_button(
            "Create JSON File", "createJsonButton", ""
        )
        self.create_json_button.clicked.connect(self.create_json_file)
        input_group_layout.addWidget(
            self.create_json_button, 0, 2
        )  # Row 0, Column 2 for the button

        # Label for New OS Version
        new_os_version_label = GUI_Factory.create_label(
            "New OS Version:", "input_label_configure_dialog"
        )
        input_group_layout.addWidget(
            new_os_version_label, 1, 0
        )  # Row 1, Column 0 for the label

        # LineEdit for new OS version input
        self.new_os_version_lineedit = GUI_Factory.create_lineedit(
            "input_lineedit_configure_dialog"
        )
        input_group_layout.addWidget(
            self.new_os_version_lineedit, 1, 1
        )  # Row 1, Column 1 for the line edit

        # Create OS Version Button
        self.create_os_version_button = GUI_Factory.create_button(
            "Create OS Version", "createOSVersionButton", ""
        )
        self.create_os_version_button.clicked.connect(
            self.create_os_version
        )  # Connect to the function
        input_group_layout.addWidget(
            self.create_os_version_button, 1, 2
        )  # Row 1, Column 2 for the button

        # Create Command Button
        self.create_command_button = GUI_Factory.create_button(
            "Create Command", "createCommandButton", ""
        )
        self.create_command_button.clicked.connect(
            self.add_command
        )  # Connect to the add_command function
        input_group_layout.addWidget(
            self.create_command_button, 2, 0, 1, 3
        )  # Place it in Row 2, Column 2

        return input_group_widget

    def __setup_scroll_area(self):
        # Create a scroll area for commands
        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        # Create a container for command entries
        self.command_container = QtWidgets.QWidget()
        self.scroll_area_layout = QtWidgets.QVBoxLayout(self.command_container)
        self.scroll_area.setWidget(self.command_container)

        # Add the scroll area to the layout
        self.layout.addWidget(self.scroll_area, 4, 0, 1, 2)  # Span across two columns

    def __setup_buttons(self):
        # Button layout
        button_layout = QtWidgets.QHBoxLayout()

        # Save button
        self.save_button = GUI_Factory.create_button("Save", "acceptButton", "")
        self.save_button.clicked.connect(self.save_changes)
        button_layout.addWidget(self.save_button)

        # Cancel button
        self.cancel_button = GUI_Factory.create_button("Cancel", "cancelButton", "")
        self.cancel_button.clicked.connect(self.handle_cancel)  # Update connection
        button_layout.addWidget(self.cancel_button)
        self.layout.addLayout(
            button_layout, 5, 0, 1, 2
        )  # Add buttons below the scroll area

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
            GUI_Factory.create_critical_message_box
            QtWidgets.QMessageBox.critical(
                self._widget_parent, "Error", "Error loading commands."
            )

    def create_os_version(self):
        """Create a new OS version object in the JSON file."""
        new_os_version = self.new_os_version_lineedit.text().strip()

        # Check if the new OS version is provided
        if not new_os_version:
            QtWidgets.QMessageBox.warning(
                self._widget_parent,
                "Warning",
                "Please enter a new OS version.",
            )
            return

        # Check if the OS version already exists
        if new_os_version in self.json_handler.os_template:
            QtWidgets.QMessageBox.warning(
                self._widget_parent,
                "Warning",
                f"OS version '{new_os_version}' already exists.",
            )
            return

        # Create an empty command structure
        command_structure = {}

        # Add the new OS version with the empty command structure to the json_handler
        self.json_handler.os_template[new_os_version] = command_structure

        # Write the updated template back to the JSON file
        self.json_handler.write_json_file(self.json_file_dropdown.currentText())

        # Notify the user
        QtWidgets.QMessageBox.information(
            self._widget_parent,
            "Success",
            f"OS version '{new_os_version}' created successfully.",
        )

        # Re-read the JSON file to update the OS version dropdown
        self.json_handler.read_json_file(self.json_file_dropdown.currentText())

        # Update the OS version dropdown with the new list of OS versions
        self.os_version_dropdown.clear()
        self.os_version_dropdown.addItems(self.json_handler.get_os_keys())

        # Select the newly created OS version in the dropdown
        self.os_version_dropdown.setCurrentText(new_os_version)

        # Optionally, clear the line edit for the next entry
        self.new_os_version_lineedit.clear()

    def handle_cancel(self):
        """Handle the cancel button click to discard changes and update command list."""
        # Check if a JSON file is selected
        selected_json = self.json_file_dropdown.currentText()
        if selected_json:
            # Re-read the JSON file to update the command list
            self.json_handler.read_json_file(selected_json)
            self.update_command_list()  # Refresh the command list
        else:
            # Reject the dialog if no file is selected
            self.OS_template_configure_page_dialog.reject()

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
                self.no_command_label = None  # Reset no command label
            else:
                # Display no commands available
                self.no_command_label = GUI_Factory.create_label(
                    "No commands available for this OS version.", "input_label"
                )
                self.scroll_area_layout.addWidget(self.no_command_label)

        except Error.JsonOSTemplateError as e:
            print(e)
            QtWidgets.QMessageBox.critical(
                self._widget_parent, "Error", "Error loading commands."
            )

    def clear_command_container(self):
        """Clear the old command container from the scroll area."""
        # Properly remove the existing widgets
        self.scroll_area.setWidget(None)  # Detach the old widget
        if self.command_container:
            self.command_container.deleteLater()  # Delete the old container

        # Reinitialize the command container and layout
        self.command_container = QtWidgets.QWidget()
        self.scroll_area_layout = QtWidgets.QGridLayout(self.command_container)
        self.scroll_area.setWidget(
            self.command_container
        )  # Reassign the new container to scroll areassign the new container to scroll areaassign the new container to scroll area

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
        command_text_edit.setText(command_data["command"])  # Set initial command

        # Checkbox for activation
        active_checkbox = QtWidgets.QCheckBox("Activate")
        active_checkbox.setObjectName(
            f"activeCheckbox_{index}"
        )  # Unique name for each checkbox
        active_checkbox.setChecked(command_data["active"])

        # Create a delete button
        delete_button = GUI_Factory.create_button("Delete", "deleteButton")
        delete_button.clicked.connect(lambda: self.delete_command_entry(index))

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
        self.scroll_area_layout.addWidget(
            delete_button, index, 3
        )  # Column 3 for delete button

    def update_json_file_dropdown(self):
        """Update the JSON file dropdown with the latest file list."""
        self.json_handler.get_list_of_file()  # Refresh the file list

        # Check if there are files in the directory before updating the dropdown
        if self.json_handler.file_list:
            self.json_file_dropdown.clear()  # Clear existing items
            self.json_file_dropdown.addItems(
                sorted(self.json_handler.file_list)
            )  # Sort and add new items
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

        # Define the file path
        file_path = os.path.join("command_template", f"{brand_name}.json")

        if os.path.exists(file_path):
            GUI_Factory.create_warning_message_box(
                self._widget_parent, "Warning", "File already exists."
            )
            return

        # Create JSON structure with OS version as an object
        json_content = {os_version: {}}

        with open(file_path, "w") as json_file:
            json.dump(json_content, json_file, indent=4)
        GUI_Factory.create_info_message_box(
            self._widget_parent,
            "Success",
            f"JSON file '{brand_name}.json' created successfully.",
        )

        # Reload the file list and update the dropdown
        self.update_json_file_dropdown()

        # Set the newly created file as the current selection in the dropdown
        self.json_file_dropdown.setCurrentText(
            brand_name + ".json"
        )  # Select the newly created JSON file

        # Update the OS version dropdown based on the newly created JSON file
        self.json_handler.read_json_file(
            self.json_file_dropdown.currentText()
        )  # Read the newly created JSON file
        self.os_version_dropdown.clear()  # Clear existing OS versions
        self.os_version_dropdown.addItems(
            self.json_handler.get_os_keys()
        )  # Add new OS keys
        self.os_version_dropdown.setCurrentText(os_version)  # Select the new OS version

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

        # Create a placeholder command structure
        command_data = {
            "command": "",  # Placeholder, can be empty or set to a default
            "active": True,  # Default to active; you can modify as needed
        }

        # Remove the "No commands available" label if it exists
        if hasattr(self, "no_command_label") and self.no_command_label is not None:
            self.no_command_label.deleteLater()  # Properly remove it from layout
            self.no_command_label = None

        # Use count() to get the number of widgets in the layout
        row_count = self.scroll_area_layout.count()

        # Simulate adding the command to the scroll area (ensure it goes in the first available position)
        self.__create_command_entry(command_title, command_data, row_count)
        GUI_Factory.create_info_message_box(
            self._widget_parent,
            "Success",
            f"Command '{command_title}' added successfully.",
        )

    def delete_command_entry(self, index: int):
        """Delete the command entry at the specified index."""
        # Remove the widgets for the command entry
        for i in range(
            4
        ):  # Assuming there are 4 widgets per row (label, text edit, checkbox, delete button)
            item = self.scroll_area_layout.itemAt(index)
            if item is not None:
                widget = item.widget()
                widget.deleteLater()  # Properly delete the widget
                self.scroll_area_layout.removeItem(item)  # Remove it from the layout

        # Re-adjust the layout after deletion
        self.update_command_list()  # Optional: refresh the command list to ensure proper indexing

    def save_changes(self):
        """Save changes to the JSON file."""
        os_key = self.os_version_dropdown.currentText()
        if os_key == "":
            GUI_Factory.create_warning_message_box(
                self._widget_parent, "Warning", "Please select an OS version first."
            )
            return

        commands = {}  # Dictionary to hold command entries

        # Iterate through each command entry in the scroll area
        for i in range(
            self.scroll_area_layout.count() // 4
        ):  # Each entry has 4 widgets
            command_label_widget = self.scroll_area_layout.itemAt(
                i * 4
            ).widget()  # Label
            command_text_edit = self.scroll_area_layout.itemAt(
                i * 4 + 1
            ).widget()  # Text edit
            active_checkbox = self.scroll_area_layout.itemAt(
                i * 4 + 2
            ).widget()  # Checkbox

            # Now we can safely access the widgets' values
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
        GUI_Factory.create_info_message_box(
            self._widget_parent, "Save", "Changes saved successfully."
        )

    def exec_(self):
        return self.OS_template_configure_page_dialog.exec_()
