import sys

import numpy
import cv2
from PySide6 import QtWidgets, QtCore
from PySide6.QtWidgets import QWidget

from ocvl.fixation.nuclear_panel import NuclearDisplay


class NuclearBase(QWidget):
    def __init__(self):
        super().__init__()


        self.layout = QtWidgets.QHBoxLayout(self)
        self.layout.addWidget(NuclearDisplay())



if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    base = NuclearBase()
    base.resize(800,500)
    base.show()

    sys.exit(app.exec())

