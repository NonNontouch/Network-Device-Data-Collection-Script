import os
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from src.communication import connection_manager
from src.factory.gui_factory import GUI_Factory
from src.pages.main_page import MainPage
from src.style import main_style


class GUI:

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
            self.Window.setObjectName("main_window")
            self.Window.setStyleSheet(main_style)
            self.Window.setWindowTitle("Network Device Data Collection Script")

            icon_path = os.path.abspath("./src/Assets/AppIcon.png")
            if os.path.exists(icon_path):  # Check if the icon file exists
                self.App.setWindowIcon(QtGui.QIcon(icon_path))
                self.Window.setWindowIcon(
                    QtGui.QIcon(icon_path)
                )  # Set icon for the window
            else:
                print(f"Icon file not found: {icon_path}")

            self._connection_manager = connection_manager()
        except Exception as e:
            print(e)

    def setup_window(self):
        self.Main_Page = MainPage(self.Window, self._connection_manager)

        self.Window.setCentralWidget(self.Main_Page.get_widget())

        self.Window.show()
        GUI_Factory.center_window(self.Window)
        sys.exit(self.App.exec_())
