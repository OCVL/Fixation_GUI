import sys
from queue import Queue

from PySide6 import QtWidgets, QtCore
from PySide6.QtGui import Qt
from PySide6.QtWidgets import QWidget
from ocvl.fixation.nuclear_panel import NuclearDisplay
from ocvl.fixation.nuclear_panel import TargetArea
from ocvl.fixation.initial_window import InitialDialog
import variable_properties
from ocvl.fixation.nuclear_target import NuclearTarget
from ocvl.fixation.server import Server
from ocvl.fixation.client import Client
from ocvl.fixation.queue_management import QueueMgmt
import threading


class NuclearBase(QWidget):
    def __init__(self, source=0):
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
        self.j = NuclearDisplay(self.var)
        self.layout.addWidget(self.j)

        self.keylist = []
        self.firstrelease = None
        self.send_again = None

        # The number of ppd of the screen we'll be projecting to (e.g. Lightcrafter, Projector, etc).
        self.var.screen_ppd = float(self.var.config.get("test", "screen_ppd"))

        # The increment steps we'll use.
        increments = self.var.config.get("test", "major_minor_increments").split("/")
        self.major_increment = float(increments[0])
        self.minor_increment = float(increments[1])

        if source == 1:
            # call the server host on a new thread if started through nuclear base
            self.x = threading.Thread(target=Server)
            self.x.daemon = True
            self.x.start()

        # thread for the client - test savior -- comment out for actual use; testing purposes only
        print("hiiii")
        self.y = threading.Thread(target=Client, args=(self.var,))
        self.y.daemon = True
        self.y.start()
        #
        self.z = threading.Thread(target=QueueMgmt, args=(self.var,))
        self.z.daemon = True
        self.z.start()





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
        self.prev_x = self.var.x_val
        self.prev_y = self.var.y_val

        if self.var.device == 'MEAO':
            if key == [QtCore.Qt.Key_Left]:
                self.var.y_val = self.var.y_val + self.major_increment
            elif key == [QtCore.Qt.Key_Up]:
                self.var.x_val = self.var.x_val - self.major_increment
            elif key == [QtCore.Qt.Key_Right]:
                self.var.y_val = self.var.y_val - self.major_increment
            elif key == [QtCore.Qt.Key_Down]:
                self.var.x_val = self.var.x_val + self.major_increment

            # shift + arrow for minor increment
            elif key == [QtCore.Qt.Key_Shift, QtCore.Qt.Key_Left]:
                self.var.y_val = self.var.y_val + self.minor_increment
            elif key == [QtCore.Qt.Key_Shift, QtCore.Qt.Key_Up]:
                self.var.x_val = self.var.x_val - self.minor_increment
            elif key == [QtCore.Qt.Key_Shift, QtCore.Qt.Key_Right]:
                self.var.y_val = self.var.y_val - self.minor_increment
            elif key == [QtCore.Qt.Key_Shift, QtCore.Qt.Key_Down]:
                self.var.x_val = self.var.x_val + self.minor_increment

        else:

            if key == [QtCore.Qt.Key_Left]:
                self.var.x_val = self.var.x_val - self.major_increment
            elif key == [QtCore.Qt.Key_Up]:
                self.var.y_val = self.var.y_val + self.major_increment
            elif key == [QtCore.Qt.Key_Right]:
                self.var.x_val = self.var.x_val + self.major_increment
            elif key == [QtCore.Qt.Key_Down]:
                self.var.y_val = self.var.y_val - self.major_increment

            # shift + arrow for minor increment
            elif key == [QtCore.Qt.Key_Shift, QtCore.Qt.Key_Left]:
                self.var.x_val = self.var.x_val - self.minor_increment
            elif key == [QtCore.Qt.Key_Shift, QtCore.Qt.Key_Up]:
                self.var.y_val = self.var.y_val + self.minor_increment
            elif key == [QtCore.Qt.Key_Shift, QtCore.Qt.Key_Right]:
                self.var.x_val = self.var.x_val + self.minor_increment
            elif key == [QtCore.Qt.Key_Shift, QtCore.Qt.Key_Down]:
                self.var.y_val = self.var.y_val - self.minor_increment


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
    base = NuclearBase(1)
    # base.resize(1000, 500)
    base.show()
    base.setFocusPolicy(Qt.StrongFocus)
    sys.exit(app.exec())

