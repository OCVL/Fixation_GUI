
import json
import os
import sys
from PySide6 import QtCore, QtWidgets
from PySide6.QtGui import Qt
from PySide6.QtWidgets import QMainWindow, QGridLayout, QWidget

from ocvl.fixation.nuclear_controls import ControlPanel
from ocvl.fixation.nuclear_notes import NotesPanel
from ocvl.fixation.fixation_display import FixationDisplay


class CenterPanel(QWidget):
    def __init__(self, parent=None, config=None):
        super(CenterPanel, self).__init__(parent)

        if config is None:
            self.config = dict()

        self.layout = QGridLayout(self)

        self.fix_disp = FixationDisplay(self.config)

        self.control_panel = ControlPanel(self.config)

        self.notes_panel = NotesPanel(self.config)

        # Connections between



        self.layout.addWidget(self.fix_disp, 0, 0)
        self.layout.addWidget(self.control_panel, 0, 1)
        self.layout.addWidget(self.notes_panel, 1, 1, 1, 2)


class NuclearBase(QMainWindow):
    def __init__(self):
        super(NuclearBase).__init__()

        with open(os.getcwd() + "\\settings.json", 'r') as config_json_path:
            self.config = json.load(config_json_path)

        self.center_panel = CenterPanel(self, self.config)
        self.setCentralWidget(self.center_panel)

        self.keylist = []
        self.firstrelease = None
        self.send_again = None

        # The increment steps we'll use.
        self.major_increment = self.config.getfloat("ui", "major_increment", fallback=1.0)
        self.minor_increment = self.config.getfloat("ui", "major_increment", fallback=0.5)

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
            self.var.x_pos_deg = self.var.x_pos_deg - self.major_increment
        elif key == [QtCore.Qt.Key_Right]:
            self.var.y_val = self.var.y_val - self.major_increment
        elif key == [QtCore.Qt.Key_Down]:
            self.var.x_pos_deg = self.var.x_pos_deg + self.major_increment

        # shift + arrow for minor increment
        elif key == [QtCore.Qt.Key_Shift, QtCore.Qt.Key_Left]:
            self.var.y_val = self.var.y_val + self.minor_increment
        elif key == [QtCore.Qt.Key_Shift, QtCore.Qt.Key_Up]:
            self.var.x_pos_deg = self.var.x_pos_deg - self.minor_increment
        elif key == [QtCore.Qt.Key_Shift, QtCore.Qt.Key_Right]:
            self.var.y_val = self.var.y_val - self.minor_increment
        elif key == [QtCore.Qt.Key_Shift, QtCore.Qt.Key_Down]:
            self.var.x_pos_deg = self.var.x_pos_deg + self.minor_increment


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

