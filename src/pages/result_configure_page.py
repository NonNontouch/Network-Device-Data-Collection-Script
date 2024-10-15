from PyQt5 import QtCore, QtGui, QtWidgets
from src.factory.gui_factory import GUI_Factory


class ResultImageConfigurePage:

    def __init__(self, widget_parent: QtWidgets.QMainWindow, curr_conf: dict) -> None:
        self._widget_parrent = widget_parent
        self.result_image_configure_page_dialog = QtWidgets.QDialog(widget_parent)
        self.result_image_configure_page_dialog.setObjectName("main_bg_color")
        self.result_image_configure_page_grid_layout = QtWidgets.QGridLayout(
            self.result_image_configure_page_dialog
        )
        self.result_image_configure_page_dialog.setWindowTitle("Image Configure")

        # Initialize properties from curr_conf
        self.bg_color = tuple(
            curr_conf.get("bg_color", (0, 0, 0))
        )  # Default to black if not set
        self.text_color = tuple(
            curr_conf.get("text_color", (255, 255, 255))
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
            self._widget_parrent, "input_widget", "", 220, 500, 400
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
            self._widget_parrent, "input_widget", "", 40, 500, 100
        )

        self.button_grid = QtWidgets.QGridLayout(self.button_widget)

        self.apply_button = GUI_Factory.create_button("Apply", "acceptButton", "")
        self.cancel_button = GUI_Factory.create_button("Cancel", "cancelButton", "")

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
