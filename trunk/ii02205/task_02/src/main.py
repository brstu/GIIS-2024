import sys
from window import MainWindow
from PySide6 import QtWidgets

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())
