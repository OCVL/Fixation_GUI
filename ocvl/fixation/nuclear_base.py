import sys

import numpy
import cv2
from PySide6 import QtWidgets, QtCore
from PySide6.QtWidgets import QWidget

from ocvl.fixation.nuclear_panel import NuclearDisplay
from ocvl.fixation.initial_window import InitialDialog
import variable_properties


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


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    base = NuclearBase()
    base.resize(1000,500)
    base.show()
    sys.exit(app.exec())

