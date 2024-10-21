import sys
from PyQt5 import QtWidgets
from src.style import main_style


class DebugWindow(QtWidgets.QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setObjectName("main_bg_color")
        self.setWindowTitle("Debug Output")
        self.setGeometry(100, 100, 600, 400)  # Set size and position

        # Create a QTextEdit to display debug output
        self.text_edit = QtWidgets.QTextEdit(self)
        self.text_edit.setObjectName("debug_textedit")
        self.text_edit.setReadOnly(True)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.text_edit)
        self.setLayout(layout)

        # Redirect stdout to the QTextEdit
        self.original_stdout = sys.stdout  # Save the original stdout
        sys.stdout = self  # Redirect stdout to this instance

    def write(self, message):
        """Write message to the QTextEdit and ensure it auto-scrolls."""
        self.text_edit.append(message)
        # Scroll to the bottom
        self.text_edit.verticalScrollBar().setValue(
            self.text_edit.verticalScrollBar().maximum()
        )

    def closeEvent(self, event):
        """Restore stdout when the debug window is closed."""
        sys.stdout = self.original_stdout  # Restore original stdout
        event.accept()  # Accept the close event

    def contextMenuEvent(self, event):
        """Create a context menu for the QTextEdit."""
        context_menu = QtWidgets.QMenu(self)

        clear_action = context_menu.addAction("Clear")
        action = context_menu.exec_(event.globalPos())

        if action == clear_action:
            self.text_edit.clear()  # Clear the QTextEdit content
