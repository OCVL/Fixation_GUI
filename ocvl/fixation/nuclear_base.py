
import json
import os
import sys
from PySide6 import QtWidgets
from PySide6.QtCore import Signal, QPointF, QObject, QEvent
from PySide6.QtGui import Qt, QKeyEvent
from PySide6.QtWidgets import QMainWindow, QGridLayout, QWidget

from ocvl.fixation.nuclear_controls import ControlPanel
from ocvl.fixation.nuclear_notes import NotesPanel
from ocvl.fixation.fixation_display import FixationDisplay


class CenterPanel(QWidget):
    positionChanged = Signal(QPointF)

    def __init__(self, config: dict = None, parent: QWidget = None):
        super().__init__(parent)

        if config is None:
            self.config = dict()
        else:
            self.config = config

        fixation_conf = self.config.get("fixation_target", dict())

        self.layout = QGridLayout(self)

        self.fix_disp = FixationDisplay(fixation_conf, self)

        self.control_panel = ControlPanel(self.config)

        # self.notes_panel = NotesPanel(self.config)

        # Connections
        self.positionChanged.connect(self.fix_disp.onPositionChanged)

        self.layout.addWidget(self.fix_disp, 0, 0)
        self.layout.addWidget(self.control_panel, 0, 1)
        #self.layout.addWidget(self.notes_panel, 1, 1, 1, 2)

        # The increment steps we'll use.
        self.major_increment = fixation_conf.get("major_increment", 0.5)
        self.minor_increment = fixation_conf.get("minor_increment", 0.1)
        self.keyboard_enabled = config.get("allow_keyboard_movement", False)


class NuclearBase(QMainWindow):

    arrowPressed = Signal(QPointF)

    def __init__(self):
        super().__init__()

        with open(os.getcwd() + "\\settings.json", 'r') as config_json_path:
            self.config = json.load(config_json_path)

        self.center_panel = CenterPanel(self.config, self)
        self.setCentralWidget(self.center_panel)

        self.keylist = []
        self.firstrelease = None
        self.send_again = None


    # Handles when the red X is clicked. Has it save some things before actually quitting
    # https://stackoverflow.com/questions/24532043/proper-way-to-handle-the-close-button-in-a-main-window-pyqt-red-x
    def closeEvent(self, event):
        print("User has clicked the red x on the main window")
        # if AOIP call to convert notes to pdf

        # closes the secondary target screen
        self.w.close()
        event.accept()
        sys.exit()

class BigBrotherListener(QObject):
    def __init__(self, little_brother: CenterPanel = None):
        super().__init__()
        self.little_brother = little_brother

    def eventFilter(self, watched, event):


        if event.type() == QEvent.KeyPress and self.little_brother.keyboard_enabled and not event.isAutoRepeat():
            key = event.key()

            old_pos = self.little_brother.fix_disp.getPosition()
            new_pos = QPointF()

            increment = self.little_brother.major_increment

            # shift + arrow for minor increment
            if event.modifiers() == Qt.ShiftModifier:
                increment = self.little_brother.minor_increment

            match key:
                case Qt.Key_Left:
                    new_pos = QPointF(old_pos.x() - increment, old_pos.y())
                case Qt.Key_Up:
                    new_pos = QPointF(old_pos.x(), old_pos.y() + increment)
                case Qt.Key_Right:
                    new_pos = QPointF(old_pos.x() + increment, old_pos.y())
                case Qt.Key_Down:
                    new_pos = QPointF(old_pos.x(), old_pos.y() - increment)

            print(f"Old: {old_pos}, New: {new_pos}")
            self.little_brother.positionChanged.emit(new_pos)
            return True

        # Call the base class implementation for other events
        return super().eventFilter(watched, event)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    base = NuclearBase()
    bigbro = BigBrotherListener(base.center_panel)
    app.installEventFilter(bigbro)

    base.setFocusPolicy(Qt.StrongFocus)
    base.show()
    sys.exit(app.exec())

