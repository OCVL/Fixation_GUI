import sys
from PySide6 import QtWidgets, QtCore
from PySide6.QtWidgets import QWidget
from ocvl.fixation.nuclear_panel import NuclearDisplay
from ocvl.fixation.nuclear_panel import TargetArea
from ocvl.fixation.initial_window import InitialDialog
import variable_properties
from ocvl.fixation.nuclear_target import NuclearTarget


class NuclearBase(QWidget):
    def __init__(self):
        super().__init__()
        # get the instance of the variables class to pass to everything
        var = variable_properties.Variables()

        # create the initial dialog window
        dlg = InitialDialog(var)
        dlg.exec()
        self.layout = QtWidgets.QHBoxLayout(self)
        self.layout.addWidget(NuclearDisplay(var))

        # call to make a new window
        self.w = NuclearTarget()
        self.w.show()

    # Handles when the red X is clicked. Has it save some things before actually quitting
    # https://stackoverflow.com/questions/24532043/proper-way-to-handle-the-close-button-in-a-main-window-pyqt-red-x
    def closeEvent(self, event):
        print("User has clicked the red x on the main window")
        # if AOIP call to convert notes to pdf

        # closes the secondary target screen
        self.w.close()

        event.accept()


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    base = NuclearBase()
    base.resize(1000, 500)
    base.show()
    sys.exit(app.exec())

