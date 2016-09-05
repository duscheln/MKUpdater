import sys # We need sys so that we can pass argv to QApplication

from PyQt5 import QtWidgets
# it also keeps events etc that we defined in Qt Designer
from main_window import ExampleApp

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)  # A new instance of QApplication
    dialog = QtWidgets.QDialog()

    prog = ExampleApp(dialog)

    dialog.show()
    sys.exit(app.exec_())

