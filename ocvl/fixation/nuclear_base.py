import sys

import numpy
import cv2
from PySide6 import QtWidgets, QtCore
from PySide6.QtWidgets import QWidget

from ocvl.fixation.nuclear_panel import NuclearDisplay
from ocvl.fixation.initial_window import InitialDialog
import test_properties


class NuclearBase(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QtWidgets.QHBoxLayout(self)
        self.layout.addWidget(NuclearDisplay())


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    var = test_properties.Variables()
    var.horz = 35.8
    print(var.horz)
    base = NuclearBase()
    base.resize(1000,500)
    base.show()

    sys.exit(app.exec())

