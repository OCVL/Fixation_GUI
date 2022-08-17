from PySide6 import QtWidgets, QtCore
from PySide6.QtCore import QPoint
from PySide6.QtGui import QPainter, Qt
from PySide6.QtWidgets import QWidget
import numpy as np


class NuclearDisplay(QWidget):
    def __init__(self):
        super().__init__()

        self.target_area = TargetArea()
        self.lefty = TargetLefty()
        self.righty = TargetRighty()

        self.layout = QtWidgets.QHBoxLayout(self)
        self.layout.addWidget(self.lefty, 2.5)
        self.layout.addWidget(self.target_area, 5)
        self.layout.addWidget(self.righty, 2.5)

    @QtCore.Slot()
    def updateTarget(self):
        pass

    @QtCore.Slot()
    def gridSizeInDeg(self):
        pass

class TargetArea(QWidget):
    def __init__(self):
        super().__init__()



    def paintEvent(self, arg__0):

        painter = QPainter(self)
        painter.setBrush(Qt.darkGray)
        painter.setRenderHint(QPainter.Antialiasing, True)

        rect = painter.window()

        radii = np.minimum(rect.width(), rect.height())/2
        cent = QPoint(rect.width()/2, rect.height()/2)

        painter.drawEllipse(cent, radii, radii)

        widthsteps = np.linspace(0, rect.width(), 30)
        heightsteps = np.linspace(0, rect.height(), 30)

        for x in widthsteps:
            pass



class TargetLefty(QWidget):
    def __init__(self):
        super().__init__()

        self.target = QtWidgets.QLabel("Sup beaches", alignment=QtCore.Qt.AlignCenter)

        self.layout = QtWidgets.QHBoxLayout(self)
        self.layout.addWidget(self.target)

    def paintEvent(self, arg__0):
        pass
        # painter = QPainter(self)
        # painter.setBrush(Qt.cyan)
        # painter.setRenderHint(QPainter.Antialiasing, True)
        #
        # rect = painter.window()
        #
        # radii = np.minimum(rect.width(), rect.height())/2
        # cent = QPoint(rect.width()/2, rect.height()/2)
        #
        # painter.drawEllipse(cent, radii, radii)


class TargetRighty(QWidget):
    def __init__(self):
        super().__init__()

        self.target = QtWidgets.QLabel("Sup beaches", alignment=QtCore.Qt.AlignCenter)

        self.layout = QtWidgets.QHBoxLayout(self)
        self.layout.addWidget(self.target)

    def paintEvent(self, arg__0):
        pass
        # painter = QPainter(self)
        # painter.setBrush(Qt.cyan)
        # painter.setRenderHint(QPainter.Antialiasing, True)
        #
        # rect = painter.window()
        #
        # radii = np.minimum(rect.width(), rect.height())/2
        # cent = QPoint(rect.width()/2, rect.height()/2)
        #
        # painter.drawEllipse(cent, radii, radii)
