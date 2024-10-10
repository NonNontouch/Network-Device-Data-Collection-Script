import os
import platform
import subprocess
import tempfile
from PyQt5 import QtCore, QtGui, QtWidgets
from src.factory.gui_factory import GUI_Factory
from src.text_to_pic_module import text_to_pic
from src.pages.result_configure_page import ResultImageConfigurePage


class ResultPage:
    def __init__(self, widget_parent, result: dict) -> None:
        self._widget_parent = widget_parent
        self.result_page_dialog = QtWidgets.QDialog(widget_parent)
        self.result_page_dialog.setObjectName("main_bg_color")
        self.result_page_dialog.setWindowTitle("Result Viewer")
        self._result = result
        self.text_to_picture = text_to_pic()  # Instance of text_to_pic
        self.temp_image_paths = []  # To store paths of temp images
        self.main_grid = QtWidgets.QGridLayout()
        self.set_configure_grid()

    def set_result(self, result: dict):
        self._result = result

    def set_configure_grid(self):
        result_configure_widget = GUI_Factory.create_widget(
            self._widget_parent, "result_configure_widget", "", 50, 600
        )
        result_configure_grid = QtWidgets.QGridLayout(result_configure_widget)
        configure_button = GUI_Factory.create_button(
            "Result Image Configure", "popup_dialog_button"
        )
        configure_button.clicked.connect(self.show_image_configure_page)
        result_configure_grid.addWidget(configure_button, 0, 0)
        self.main_grid.addWidget(result_configure_widget, 0, 0)

    def show_image_configure_page(self):
        dialog = ResultImageConfigurePage(
            self._widget_parent, self.text_to_picture.get_cur_config()
        )

        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            user_input = dialog.get_input()
            print(user_input)
            # Set new parameters for image generation
            self.text_to_picture.set_parameters(user_input)

            # Clean up old temporary images before generating new ones
            self.cleanup_temp_images()

            # Clear the list of temp image paths after deleting old images
            self.temp_image_paths.clear()

            # Generate new images based on the updated configuration
            self.generate_all_image()

            # Rebuild the result grid with the updated temp image paths
            self.reset_result_grid()

    def reset_result_grid(self):
        """Clears the result grid and sets it up again with updated image paths."""
        # Remove the current widgets in the grid
        for i in reversed(range(self.main_grid.count())):
            widget = self.main_grid.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()  # Ensure the widget is properly deleted

        # Recreate the result grid layout with updated temp image paths
        self.set_configure_grid()
        self.set_result_grid()

    def set_result_grid(self):
        # Create the main grid layout
        # Create a widget to hold the results
        self.scroll_area = QtWidgets.QScrollArea()
        result_widget = GUI_Factory.create_widget(
            self._widget_parent, "main_window", ""
        )
        results_layout = QtWidgets.QGridLayout(result_widget)

        # Create a scroll area
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(
            result_widget
        )  # Set the result widget as the scroll area content

        # Populate the results content with buttons for each result
        i = 0
        for title, result in self._result.items():
            if "An error occurred while executing the" in result:
                sub_widget = GUI_Factory.create_widget(
                    self._widget_parent,
                    "result_widget_error",
                    "",
                    170,
                    350,
                )
            else:
                sub_widget = GUI_Factory.create_widget(
                    self._widget_parent,
                    "single_result_widget",
                    "",
                    170,
                    350,
                )
            sub_grid = QtWidgets.QGridLayout(sub_widget)
            command_banner = GUI_Factory.create_label(
                f"{title}",
                "label_banner",
                alignment=QtCore.Qt.AlignCenter,
                HorSizePolicy=QtWidgets.QSizePolicy.Expanding,
                VerSizePolicy=QtWidgets.QSizePolicy.Preferred,
            )
            sub_grid.addWidget(command_banner, 0, 0, 1, 2)

            if "show tech-support" in title.lower():
                # If the title is "show tech-support", do not generate the image
                # Only create the Save Text button
                save_text_button = GUI_Factory.create_button(
                    f"Save {title} Text", "result_button_save_text"
                )
                save_text_button.clicked.connect(
                    lambda checked, text=result, title=title: self.save_text(
                        text, title
                    )
                )
                sub_grid.addWidget(
                    save_text_button, 1, 0, 1, 2
                )  # Span across both columns
            else:
                # Create a temporary file to hold the generated image

                # Create a button to preview the image
                preview_button = GUI_Factory.create_button(
                    f"Preview {title} Image", "result_button_preview"
                )
                preview_button.clicked.connect(
                    lambda checked, img_path=self.temp_image_paths[
                        i
                    ]: self.preview_image(img_path)
                )
                sub_grid.addWidget(preview_button, 1, 0, 1, 2)

                # Create a button to save the image
                save_image_button = GUI_Factory.create_button(
                    f"Save Image", "result_button_save_image"
                )

                save_image_button.clicked.connect(
                    lambda checked, img_path=self.temp_image_paths[
                        i
                    ], title=title: self.save_image(img_path, title)
                )
                sub_grid.addWidget(save_image_button, 2, 0)

                # Create a button to save the text
                save_text_button = GUI_Factory.create_button(
                    f"Save Text", "result_button_save_text"
                )
                save_text_button.clicked.connect(
                    lambda checked, text=result, title=title: self.save_text(
                        text, title
                    )
                )
                sub_grid.addWidget(save_text_button, 2, 1)  # Add to the right column

            results_layout.addWidget(sub_widget, i, 0)
            i += 1

        # Add the scroll area to the main grid layout

        self.main_grid.addWidget(self.scroll_area, 1, 0)

        # Set the main layout to the dialog
        self.result_page_dialog.setLayout(self.main_grid)

    def save_text(self, text, title):
        """Open a file dialog to save the text."""
        options = QtWidgets.QFileDialog.Options()
        # Get the current working directory
        default_path = os.getcwd()
        # Set default file name
        default_file_name = f"{title}.txt"
        file_path, _ = QtWidgets.QFileDialog.getSaveFileName(
            self.result_page_dialog,
            f"Save {title} Text",
            os.path.join(default_path, default_file_name),
            "Text Files (*.txt);;All Files (*)",
            options=options,
        )
        if file_path:
            with open(file_path, "w") as file:
                file.write(text)  # Save the text to the selected path

    def save_image(self, image_path, title):
        """Open a file dialog to save the image."""
        options = QtWidgets.QFileDialog.Options()
        # Get the current working directory
        default_path = os.getcwd()
        # Set default file name based on the title
        default_file_name = f"{title}.png"  # Assuming you want to save it as a PNG
        file_path, _ = QtWidgets.QFileDialog.getSaveFileName(
            self.result_page_dialog,
            f"Save {title} Image",
            os.path.join(default_path, default_file_name),
            "Images (*.png *.jpg *.bmp);;All Files (*)",
            options=options,
        )
        if file_path:
            # Copy the temporary image to the new location
            with open(image_path, "rb") as src_file:
                with open(file_path, "wb") as dst_file:
                    dst_file.write(
                        src_file.read()
                    )  # Save the image to the selected path

    def generate_all_image(
        self,
    ):
        for title, result in self._result.items():
            self.generate_image(result)

    def generate_image(self, text: str) -> str:
        """Generate an image from the given text and return the file path."""
        import cv2

        image = self.text_to_picture.create_text_image(text)

        # Create a temporary file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
        temp_file_path = temp_file.name

        # Save the image to the temporary file
        cv2.imwrite(temp_file_path, image)  # Save the image
        temp_file.close()  # Close the temp file so it can be accessed later

        # Store the temp file path for cleanup
        self.temp_image_paths.append(temp_file_path)

        return temp_file_path  # Return the path to the temporary image

    def cleanup_temp_images(self):
        """Delete all temporary image files created."""
        for path in self.temp_image_paths:
            if os.path.exists(path):
                os.remove(path)

    def preview_image(self, image_path: str):
        """Open the image using the default image viewer."""
        # Check if the image file exists
        if os.path.exists(image_path):
            try:
                current_os = platform.system()  # Get the OS name
                if current_os == "Linux":
                    subprocess.Popen(["xdg-open", image_path])  # For Linux
                elif current_os == "Darwin":
                    subprocess.Popen(["open", image_path])  # For macOS
                elif current_os == "Windows":
                    subprocess.Popen(["start", image_path], shell=True)  # For Windows
                else:
                    GUI_Factory.create_warning_message_box(
                        self._widget_parent,
                        "Unsupported OS",
                        "This operating system is not supported for opening images.",
                    )

            except Exception as e:
                GUI_Factory.create_warning_message_box(
                    self._widget_parent, "Error", f"Failed to open image: {str(e)}"
                )

        else:
            GUI_Factory.create_warning_message_box(
                self._widget_parent,
                "File Not Found",
                f"The specified image file does not exist: {image_path}",
            )

    def exec_(self):
        """Show the result dialog and cleanup temp images on close."""
        result = self.result_page_dialog.exec_()
        self.cleanup_temp_images()  # Clean up temp images when dialog is closed
        return result
