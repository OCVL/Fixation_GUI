import configparser

from PySide6 import QtWidgets, QtCore
from PySide6.QtCore import QPoint, QRect
from PySide6.QtGui import QPainter, Qt, QPen, QColor
from PySide6.QtWidgets import QWidget
import numpy as np
from ocvl.fixation.initial_window import InitialDialog
from ocvl.fixation.nuclear_controls import Tabs
from ocvl.fixation.nuclear_notes import NuclearNotes
from ocvl.fixation.nuclear_info import NuclearInfo


class NuclearDisplay(QWidget):
    def __init__(self):
        super().__init__()

        self.sub_id = None
        self.selected_eye = None
        self.save_loc_dir = None
        self.dev_name = None
        self.config_name = None

        self.LaunchInitialDialog()

        self.target_area = TargetArea(self.config_name)
        self.lefty = TargetLefty(self.selected_eye, self.sub_id, self.save_loc_dir, self.dev_name)
        self.righty = TargetRighty()
        self.bottom = TargetBottom()

        self.layout1 = QtWidgets.QVBoxLayout(self)
        self.layout2 = QtWidgets.QHBoxLayout(self)
        self.layout2.addWidget(self.lefty)
        self.layout2.addWidget(self.target_area, 20)
        self.layout2.addWidget(self.righty)
        self.layout1.addLayout(self.layout2)
        self.layout1.addWidget(self.bottom)

    def LaunchInitialDialog(self):
        dlg = InitialDialog()
        dlg.exec()

        self.config_name = dlg.config_name  # config file name
        self.dev_name = dlg.device_selected  # device name
        self.save_loc_dir = dlg.save_location_dir  # save location directory path
        self.selected_eye = dlg.eye_selected
        self.sub_id = dlg.subject_id

    @QtCore.Slot()
    def updateTarget(self):
        pass

    @QtCore.Slot()
    def gridSizeInDeg(self):
        pass

class TargetArea(QWidget):
    def __init__(self, config_name):
        super().__init__()

        self.config = configparser.ConfigParser()
        self.config.read(config_name)
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
    def __init__(self, eye, sub_id, save_loc, device):
        super().__init__()

        # self.target = QtWidgets.QLabel("Sup beaches", alignment=QtCore.Qt.AlignCenter)
        self.target = NuclearInfo(eye, sub_id, save_loc, device)

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

        # self.target = QtWidgets.QLabel("Sup beaches", alignment=QtCore.Qt.AlignCenter)
        self.target = Tabs()

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

class TargetBottom(QWidget):
    def __init__(self):
        super().__init__()

        # self.target = QtWidgets.QLabel("Sup beaches", alignment=QtCore.Qt.AlignCenter)
        self.target = NuclearNotes()

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

