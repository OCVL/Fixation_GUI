import sys
from PySide6 import QtWidgets, QtCore
from PySide6.QtGui import Qt
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
        self.firstrelease = None
        self.send_again = None

        # The number of ppd of the screen we'll be projecting to (e.g. Lightcrafter, Projector, etc).
        self.screen_ppd = float(self.var.config.get("test", "screen_ppd"))

        # The increment steps we'll use.
        increments = self.var.config.get("test", "major_minor_increments").split("/")
        self.major_increment = float(increments[0])
        self.minor_increment = float(increments[1])



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

        if key == [QtCore.Qt.Key_Left]:
            self.var.x_val = self.var.x_val - self.major_increment
            self.var.center_x = self.var.center_x - self.major_increment * self.screen_ppd
            self.var.center_x_grid = self.var.center_x_grid - self.major_increment * self.var.grid_mult
        elif key == [QtCore.Qt.Key_Up]:
            self.var.y_val = self.var.y_val + self.major_increment
            self.var.center_y = self.var.center_y - self.major_increment * self.screen_ppd
            self.var.center_y_grid = self.var.center_y_grid - self.major_increment * self.var.grid_mult
        elif key == [QtCore.Qt.Key_Right]:
            self.var.x_val = self.var.x_val + self.major_increment
            self.var.center_x = self.var.center_x + self.major_increment * self.screen_ppd
            self.var.center_x_grid = self.var.center_x_grid + self.major_increment * self.var.grid_mult
        elif key == [QtCore.Qt.Key_Down]:
            self.var.y_val = self.var.y_val - self.major_increment
            self.var.center_y = self.var.center_y + self.major_increment * self.screen_ppd
            self.var.center_y_grid = self.var.center_y_grid + self.major_increment * self.var.grid_mult

        # shift + arrow for minor increment
        elif key == [QtCore.Qt.Key_Shift, QtCore.Qt.Key_Left]:
            self.var.x_val = self.var.x_val - self.minor_increment
            self.var.center_x = self.var.center_x - self.minor_increment * self.screen_ppd
            self.var.center_x_grid = self.var.center_x_grid - self.minor_increment * self.var.grid_mult
        elif key == [QtCore.Qt.Key_Shift, QtCore.Qt.Key_Up]:
            self.var.y_val = self.var.y_val + self.minor_increment
            self.var.center_y = self.var.center_y - self.minor_increment * self.screen_ppd
            self.var.center_y_grid = self.var.center_y_grid - self.minor_increment * self.var.grid_mult
        elif key == [QtCore.Qt.Key_Shift, QtCore.Qt.Key_Right]:
            self.var.x_val = self.var.x_val + self.minor_increment
            self.var.center_x = self.var.center_x + self.minor_increment * self.screen_ppd
            self.var.center_x_grid = self.var.center_x_grid + self.minor_increment * self.var.grid_mult
        elif key == [QtCore.Qt.Key_Shift, QtCore.Qt.Key_Down]:
            self.var.y_val = self.var.y_val - self.minor_increment
            self.var.center_y = self.var.center_y + self.minor_increment * self.screen_ppd
            self.var.center_y_grid = self.var.center_y_grid + self.minor_increment * self.var.grid_mult

        # print("previous value: ")
        # print(self.prev_x)
        # print("current value: ")
        # print(self.var.x_val)
        # # print(self.var.y_val)
        #
        # if self.prev_x > self.var.x_val:
        #     if self.var.x_val == 0:
        #         self.var.center_x = self.var.center_x_og
        #     else:
        #         self.var.center_x = self.var.center_x_og - (abs(self.var.x_val) * self.screen_ppd)
        # if self.prev_x < self.var.x_val:
        #     if self.var.x_val == 0:
        #         self.var.center_x = self.var.center_x_og
        #     else:
        #         self.var.center_x = self.var.center_x_og + (abs(self.var.x_val) * self.screen_ppd)
        # if self.prev_y != self.var.y_val:
        #     self.var.center_y = self.var.center_y - (self.var.y_val * self.screen_ppd)
        # self.var.center_x_grid =

        # if key == [QtCore.Qt.Key_Left]:
        #     self.var.center_x = self.var.center_x - self.major_increment * self.screen_ppd
        # elif key == [QtCore.Qt.Key_Up]:
        #     self.var.center_y = self.var.center_y - self.major_increment * self.screen_ppd
        # elif key == [QtCore.Qt.Key_Right]:
        #     self.var.center_x = self.var.center_x + self.major_increment * self.screen_ppd
        # elif key == [QtCore.Qt.Key_Down]:
        #     self.var.center_y = self.var.center_y + self.major_increment * self.screen_ppd
        #
        # # shift + arrow for minor increment
        # elif key == [QtCore.Qt.Key_Shift, QtCore.Qt.Key_Left]:
        #     self.var.center_x = self.var.center_x - self.minor_increment * self.screen_ppd
        # elif key == [QtCore.Qt.Key_Shift, QtCore.Qt.Key_Up]:
        #     self.var.center_y = self.var.center_y - self.minor_increment * self.screen_ppd
        # elif key == [QtCore.Qt.Key_Shift, QtCore.Qt.Key_Right]:
        #     self.var.center_x = self.var.center_x + self.minor_increment * self.screen_ppd
        # elif key == [QtCore.Qt.Key_Shift, QtCore.Qt.Key_Down]:
        #     self.var.center_y = self.var.center_y + self.minor_increment * self.screen_ppd



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
    # base.resize(1000, 500)
    base.show()
    base.setFocusPolicy(Qt.StrongFocus)
    sys.exit(app.exec())

