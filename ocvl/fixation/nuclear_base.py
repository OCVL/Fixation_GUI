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
        self.var = variable_properties.Variables()

        # create the initial dialog window
        dlg = InitialDialog(self.var)
        dlg.exec()

        # call to make a new window
        # put if statement here to know if we need this to start up from info from the config file (animal land doesn't need the secondary display)
        self.w = NuclearTarget(self.var)
        self.w.show()

        self.layout = QtWidgets.QHBoxLayout(self)
        self.layout.addWidget(NuclearDisplay(self.var))
        self.keylist = []
        # self.multi = 1



    def keyPressEvent(self, eventQKeyEvent):
        key = eventQKeyEvent.key()
        self.firstrelease = True
        self.keylist.append(key)
    def keyReleaseEvent(self, event):
        if self.firstrelease:
            self.processmultikeys(self.keylist)
        self.firstrelease = False
        del self.keylist[-1]

    def processmultikeys(self, key):

        # will need to check what increment is actually 1 deg for fixation target
        # major increment
        if key == [QtCore.Qt.Key_Left]:
            self.var.center_x = self.var.center_x - 10
        elif key == [QtCore.Qt.Key_Up]:
            self.var.center_y = self.var.center_y - 10
        elif key == [QtCore.Qt.Key_Right]:
            self.var.center_x = self.var.center_x + 10
        elif key == [QtCore.Qt.Key_Down]:
            self.var.center_y = self.var.center_y + 10

        # shift + arrow for minor increment
        elif key == [QtCore.Qt.Key_Shift, QtCore.Qt.Key_Left]:
            self.var.center_x = self.var.center_x - 5
        elif key == [QtCore.Qt.Key_Shift, QtCore.Qt.Key_Up]:
            self.var.center_y = self.var.center_y - 5
        elif key == [QtCore.Qt.Key_Shift, QtCore.Qt.Key_Right]:
            self.var.center_x = self.var.center_x + 5
        elif key == [QtCore.Qt.Key_Shift, QtCore.Qt.Key_Down]:
            self.var.center_y = self.var.center_y + 5



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

