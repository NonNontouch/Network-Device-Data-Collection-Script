import os
import platform
import subprocess
import tempfile
from PyQt5 import QtCore, QtGui, QtWidgets
from src.factory.gui_factory import GUI_Factory
from src.text_to_pic_module import text_to_pic
from src.pages.result_configure_page import ResultImageConfigurePage
from src.regular_expression_handler import data_handling


class ResultPage:
    def __init__(self, widget_parent, result: dict, connected_hostname: str) -> None:
        self._widget_parent = widget_parent
        self.connected_hostname = connected_hostname
        self.result_page_dialog = QtWidgets.QDialog(widget_parent)
        self.result_page_dialog.setObjectName("main_bg_color")
        self.result_page_dialog.setWindowTitle(f"Result Viewer of {connected_hostname}")
        self._result = result
        self.text_to_picture = text_to_pic()
        self.temp_image_paths = []
        self.main_grid = QtWidgets.QGridLayout()
        self.set_configure_grid()
        self.set_save_all_button_grid()

    def set_result(self, result: dict):
        self._result = result

    def set_configure_grid(self):
        result_configure_widget = GUI_Factory.create_widget(
            self._widget_parent, "input_widget", "", 120, 600
        )
        result_configure_grid = QtWidgets.QGridLayout(result_configure_widget)
        configure_button = GUI_Factory.create_button(
            "Edit Image", "popup_dialog_button"
        )
        configure_button.clicked.connect(self.show_image_configure_page)
        conplete_hostname_label = GUI_Factory.create_label(
            self.connected_hostname,
            "label_banner",
            alignment=QtCore.Qt.AlignCenter,
            HorSizePolicy=QtWidgets.QSizePolicy.Expanding,
            VerSizePolicy=QtWidgets.QSizePolicy.Preferred,
        )
        result_configure_grid.addWidget(
            conplete_hostname_label,
            0,
            0,
        )
        result_configure_grid.addWidget(configure_button, 1, 0)
        self.main_grid.addWidget(result_configure_widget, 0, 0)

    def show_image_configure_page(self):
        dialog = ResultImageConfigurePage(
            self._widget_parent, self.text_to_picture.get_cur_config()
        )

        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            user_input = dialog.get_input()
            print(user_input)
            self.text_to_picture.set_parameters(user_input)

            self.cleanup_temp_images()

            self.temp_image_paths.clear()

            self.generate_all_image()

            self.reset_result_grid()

    def reset_result_grid(self):
        """Clears the result grid and sets it up again with updated image paths."""

        for i in reversed(range(self.main_grid.count())):
            widget = self.main_grid.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        self.set_configure_grid()
        self.set_result_grid()
        self.set_save_all_button_grid()

    def set_result_grid(self):

        self.scroll_area = QtWidgets.QScrollArea()

        result_widget = GUI_Factory.create_widget(
            self._widget_parent, "input_widget", ""
        )
        results_layout = QtWidgets.QGridLayout(result_widget)

        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(result_widget)

        i = 0
        for title, result in self._result.items():

            object_name = "single_result_widget"

            if "show cpu usage" in title.lower():
                cpu_status = data_handling.analyze_cpu_utilization(result)
                if cpu_status == 0:
                    title = title + " (normal)"
                elif cpu_status == 1:
                    object_name = "warning_result_widget"
                    title = title + " (quite high)"
                elif cpu_status == 2:
                    object_name = "danger_result_widget"
                    title = title + " (high)"

            elif "show memory usage" in title.lower():
                memory_status = data_handling.analyze_memory_utilization(result)
                if cpu_status == 0:
                    title = title + " (normal)"
                elif memory_status == 1:
                    object_name = "warning_result_widget"
                    title = title + " (quite high)"
                elif memory_status == 2:
                    object_name = "danger_result_widget"
                    title = title + " (high)"
            if "An error occurred while executing the" in result:
                object_name = "result_widget_error"
                title = title.replace("(normal)", "(error)")

            sub_widget = GUI_Factory.create_widget(
                self._widget_parent,
                object_name,
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
                save_text_button = GUI_Factory.create_button(
                    f"Save {title} Text", "result_button_save_text"
                )
                save_text_button.clicked.connect(
                    lambda checked, text=result, title=title: self.save_text(
                        text, title
                    )
                )
                sub_grid.addWidget(save_text_button, 1, 0, 1, 2)
            else:

                preview_button = GUI_Factory.create_button(
                    f"Preview {title} Image", "result_button_preview"
                )
                preview_button.clicked.connect(
                    lambda checked, img_path=self.temp_image_paths[
                        i
                    ]: self.preview_image(img_path)
                )
                sub_grid.addWidget(preview_button, 1, 0, 1, 2)

                save_image_button = GUI_Factory.create_button(
                    f"Save Image", "result_button_save_image"
                )
                save_image_button.clicked.connect(
                    lambda checked, img_path=self.temp_image_paths[
                        i
                    ], title=title: self.save_image(img_path, title)
                )
                sub_grid.addWidget(save_image_button, 2, 0)

                save_text_button = GUI_Factory.create_button(
                    f"Save Text", "result_button_save_text"
                )
                save_text_button.clicked.connect(
                    lambda checked, text=result, title=title: self.save_text(
                        text, title
                    )
                )
                sub_grid.addWidget(save_text_button, 2, 1)

            results_layout.addWidget(sub_widget, i, 0)
            i += 1

        self.main_grid.addWidget(self.scroll_area, 1, 0)

        self.result_page_dialog.setLayout(self.main_grid)

    def set_save_all_button_grid(self):
        save_all_button_widget = GUI_Factory.create_widget(
            self._widget_parent, "input_widget", "", 80, 600
        )
        save_all_button_grid = QtWidgets.QGridLayout(save_all_button_widget)
        save_all_image_button = GUI_Factory.create_button(
            "Save All Image", "save_all_image_button"
        )
        save_all_image_button.clicked.connect(self.save_all_image)
        save_all_text_button = GUI_Factory.create_button(
            "Save All Text", "save_all_text_button"
        )
        save_all_text_button.clicked.connect(self.save_all_text)

        save_all_button_grid.addWidget(save_all_image_button, 0, 0)
        save_all_button_grid.addWidget(save_all_text_button, 0, 1)
        self.main_grid.addWidget(save_all_button_widget, 2, 0)

    def save_text(self, text, title):
        """Open a file dialog to save the text."""
        options = QtWidgets.QFileDialog.Options()

        default_file_name = f"{self.connected_hostname} {title}.txt"
        file_path, _ = QtWidgets.QFileDialog.getSaveFileName(
            self.result_page_dialog,
            f"Save {title} Text",
            default_file_name,
            "Text Files (*.txt);;All Files (*)",
            options=options,
        )
        if file_path:
            with open(file_path, "w") as file:
                file.write(text)

    def save_image(self, image_path, title):
        """Open a file dialog to save the image."""
        options = QtWidgets.QFileDialog.Options()

        default_file_name = f"{self.connected_hostname} {title}.png"
        file_path, _ = QtWidgets.QFileDialog.getSaveFileName(
            self.result_page_dialog,
            f"Save {title} Image",
            default_file_name,
            "Images (*.png *.jpg *.bmp);;All Files (*)",
            options=options,
        )
        if file_path:

            with open(image_path, "rb") as src_file:
                with open(file_path, "wb") as dst_file:
                    dst_file.write(src_file.read())

    def generate_all_image(
        self,
    ):
        for title, result in self._result.items():
            if title == "show tech-support":
                continue
            self.generate_image(result)

    def generate_image(self, text: str) -> str:
        """Generate an image from the given text and return the file path."""
        import cv2

        image = self.text_to_picture.create_text_image(text)

        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
        temp_file_path = temp_file.name

        cv2.imwrite(temp_file_path, image)
        temp_file.close()

        self.temp_image_paths.append(temp_file_path)

        return temp_file_path

    def cleanup_temp_images(self):
        """Delete all temporary image files created."""
        for path in self.temp_image_paths:
            if os.path.exists(path):
                os.remove(path)

    def preview_image(self, image_path: str):
        """Open the image using the default image viewer."""

        if os.path.exists(image_path):
            try:
                current_os = platform.system()
                if current_os == "Linux":
                    subprocess.Popen(["xdg-open", image_path])
                elif current_os == "Darwin":
                    subprocess.Popen(["open", image_path])
                elif current_os == "Windows":
                    subprocess.Popen(["start", image_path], shell=True)
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

    def save_all_image(self):
        """Open a folder dialog and save all images to the selected folder."""
        options = QtWidgets.QFileDialog.Options()
        folder_path = QtWidgets.QFileDialog.getExistingDirectory(
            self.result_page_dialog,
            "Select Folder to Save All Images",
            options=options,
        )

        if folder_path:

            for i, image_path in enumerate(self.temp_image_paths):

                title = list(self._result.keys())[i]
                filename = f"{self.connected_hostname} {title}.png"
                file_path = os.path.join(folder_path, filename)

                try:

                    with open(image_path, "rb") as src_file:
                        with open(file_path, "wb") as dst_file:
                            dst_file.write(src_file.read())
                except Exception as e:
                    GUI_Factory.create_warning_message_box(
                        self._widget_parent, "Error", f"Failed to save image: {str(e)}"
                    )
                    return
            GUI_Factory.create_info_message_box(
                self._widget_parent, "Done", "All image have been saved."
            )

    def save_all_text(self):
        """Open a folder dialog and save all text results to the selected folder."""
        options = QtWidgets.QFileDialog.Options()
        folder_path = QtWidgets.QFileDialog.getExistingDirectory(
            self.result_page_dialog,
            "Select Folder to Save All Text",
            options=options,
        )

        if folder_path:

            for title, text in self._result.items():

                filename = f"{self.connected_hostname} {title}.txt"
                file_path = os.path.join(folder_path, filename)

                try:

                    with open(file_path, "w") as file:
                        file.write(text)
                except Exception as e:
                    GUI_Factory.create_warning_message_box(
                        self._widget_parent, "Error", f"Failed to save text: {str(e)}"
                    )
            GUI_Factory.create_info_message_box(
                self._widget_parent, "Done", "All text have been saved."
            )

    def exec_(self):
        """Show the result dialog and cleanup temp images on close."""
        result = self.result_page_dialog.exec_()
        self.cleanup_temp_images()
        return result
