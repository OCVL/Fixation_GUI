import configparser
import os
import sys
from PySide6 import QtWidgets, QtCore
from PySide6.QtGui import Qt
from PySide6.QtWidgets import  QMainWindow
from ocvl.fixation.nuclear_panel import NuclearDisplay
import variable_properties
from ocvl.fixation.nuclear_target import NuclearTarget


class NuclearBase(QMainWindow):
    def __init__(self):
        super().__init__()

        # Read what we can from our settings file.
        self.config = configparser.ConfigParser()
        self.config_name = os.getcwd() + "\\settings.ini"
        self.config.read(self.config_name)


        # This... thing is effectively a global variable, and I hate everything about it, but I don't have the time
        # or interest to fix the whole code structure. -RFC
        self.var = variable_properties.StatusVariables()

        # call to make a new window
        # put if statement here to know if we need this to start up from info from the config file (animal land doesn't need the secondary display)
        self.w = NuclearTarget(self.var)
        self.w.show()

        self.layout = QtWidgets.QHBoxLayout(self)
        self.j = NuclearDisplay(self.var)
        self.setCentralWidget(self.j)

        self.keylist = []
        self.firstrelease = None
        self.send_again = None

        # The number of ppd of the screen we'll be projecting to (e.g. Lightcrafter, Projector, etc).
        self.var.screen_ppd = float(self.var.config.get("screen_ppd"))

        # The increment steps we'll use.
        self.major_increment = float(self.var.config.get("major_increment", 1.0))
        self.minor_increment = float(self.var.config.get("major_increment", 0.5))

    def keyPressEvent(self, eventQKeyEvent):
        key = eventQKeyEvent.key()
        self.firstrelease = True
        self.keylist.append(key)
        # print('pressed')
        # resending the event to keyrelease if this was called from keyRelease
        if self.send_again:
            self.send_again = False
            self.keyReleaseEvent(eventQKeyEvent)

    def keyReleaseEvent(self, event):
        if self.firstrelease:
            self.processmultikeys(self.keylist)
        self.firstrelease = False
        # resending the event to keypress if the press wasn't originally recognized
        if len(self.keylist) == 0:
            self.send_again = True
            self.keyPressEvent(event)
            return
        del self.keylist[-1]
        # print('deleted')

    def processmultikeys(self, key):
        # print(key)
        # will need to check what increment is actually 1 deg for fixation target and if multiplying by screen ppd is correct
        # major increment

        if key == [QtCore.Qt.Key_Left]:
            self.var.y_val = self.var.y_val + self.major_increment
        elif key == [QtCore.Qt.Key_Up]:
            self.var.x_pos = self.var.x_pos - self.major_increment
        elif key == [QtCore.Qt.Key_Right]:
            self.var.y_val = self.var.y_val - self.major_increment
        elif key == [QtCore.Qt.Key_Down]:
            self.var.x_pos = self.var.x_pos + self.major_increment

        # shift + arrow for minor increment
        elif key == [QtCore.Qt.Key_Shift, QtCore.Qt.Key_Left]:
            self.var.y_val = self.var.y_val + self.minor_increment
        elif key == [QtCore.Qt.Key_Shift, QtCore.Qt.Key_Up]:
            self.var.x_pos = self.var.x_pos - self.minor_increment
        elif key == [QtCore.Qt.Key_Shift, QtCore.Qt.Key_Right]:
            self.var.y_val = self.var.y_val - self.minor_increment
        elif key == [QtCore.Qt.Key_Shift, QtCore.Qt.Key_Down]:
            self.var.x_pos = self.var.x_pos + self.minor_increment


        # call to function in nuclear_controls to update the coordinate text in the control panel
        self.j.righty.target.updateCoordText()

    # Handles when the red X is clicked. Has it save some things before actually quitting
    # https://stackoverflow.com/questions/24532043/proper-way-to-handle-the-close-button-in-a-main-window-pyqt-red-x
    def closeEvent(self, event):
        print("User has clicked the red x on the main window")
        # if AOIP call to convert notes to pdf

        # closes the secondary target screen
        self.w.close()
        event.accept()
        sys.exit()


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    base = NuclearBase()
    # base.resize(1000, 500)
    base.show()
    base.setFocusPolicy(Qt.StrongFocus)
    sys.exit(app.exec())

