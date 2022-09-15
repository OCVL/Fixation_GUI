import configparser
import math

from PySide6 import QtWidgets, QtCore
from PySide6.QtCore import QPoint
from PySide6.QtGui import QPainter, Qt, QPen, QColor
from PySide6.QtWidgets import QWidget
import numpy as np
from tkinter import filedialog


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

        self.config = configparser.ConfigParser()
        self.config_name = filedialog.askopenfilenames(title='Select the configuration file', filetypes=[
            ("configuration file", ".ini")])
        self.config.read(self.config_name)
        self.grid_size = self.config.get("test", "grid_size")
        self.circle_vis = self.config.get("test", "fixation_circle_visible")



    def paintEvent(self, arg__0):

        painter = QPainter(self)
        painter.setBrush(QColor(75, 75, 75))
        painter.setRenderHint(QPainter.Antialiasing, True)

        rect = painter.window()

        radii = np.minimum(rect.width(), rect.height())/2
        cent = QPoint(rect.width()/2, rect.height()/2)
        if(self.grid_size == 'small'):
            num_of_lines = 31
        elif(self.grid_size == 'medium'):
            num_of_lines = 41
        elif(self.grid_size == 'large'):
            num_of_lines = 61
        else:
            num_of_lines = 0

        spacing = (radii*2)/num_of_lines
        painter.drawRect(rect.width() / 2 - radii, rect.height() / 2 - radii, radii * 2, radii * 2)

        horz_steps = np.linspace(rect.width()/2-radii, rect.width()/2+radii, num_of_lines)
        vert_steps = np.linspace(rect.height()/2-radii, rect.height()/2+radii, num_of_lines)

        center_line = (num_of_lines-1)/2

        counter = 0
        for y in vert_steps:
            if counter % 5 == 0:
                if counter == center_line:
                    painter.setPen(QPen(QColor(255, 79, 0), 2.5))
                else:
                    painter.setPen(QPen(QColor(255, 79, 0)))
                painter.drawLine(rect.width() / 2 - radii, y, rect.width() / 2 + radii, y)
            else:
                painter.setPen(Qt.black)
                painter.drawLine(rect.width() / 2 - radii, y, rect.width() / 2 + radii, y)
            counter += 1

        counter = 0
        for x in horz_steps:
            if counter % 5 == 0:
                if counter == center_line:
                    painter.setPen(QPen(QColor(255, 79, 0), 2.5))
                else:
                    painter.setPen(QPen(QColor(255, 79, 0)))
                painter.drawLine(x, rect.height() / 2 - radii, x, rect.height() / 2 + radii)
            else:
                painter.setPen(Qt.black)
                painter.drawLine(x, rect.height() / 2 - radii, x, rect.height() / 2 + radii)
            counter += 1

        painter.setPen(Qt.black)

        if self.circle_vis == "1":
            painter.setPen(QPen(QColor(3, 175, 224), 2.5))
            # painter.drawEllipse(cent, spacing * 15.5, spacing * 15.5)
            painter.drawArc((rect.width()/2)-(spacing * 15.25), (rect.height()/2)-(spacing * 15.25), spacing * 30.5, spacing * 30.5, 0, 16*360)
            print('')
        else:
            pass
        painter.setPen(Qt.black)


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
