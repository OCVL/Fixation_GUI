import configparser
from PySide6 import QtWidgets, QtCore
from PySide6.QtCore import QPoint, QRect
from PySide6.QtGui import QPainter, Qt, QPen, QColor
from PySide6.QtWidgets import QWidget
import numpy as np
from ocvl.fixation.nuclear_controls import Tabs
from ocvl.fixation.nuclear_notes import NuclearNotes


class NuclearDisplay(QWidget):
    def __init__(self, var):
        super().__init__()

        self.var = var

        # setting up GUI panels
        # self.lefty = TargetLefty(self.selected_eye, self.sub_id, self.save_loc_dir, self.dev_name)
        self.righty = TargetRighty(self.var)
        self.bottom = TargetBottom(self.var)

        # Get the dims from the Configuration tabs
        var.dim = self.righty.target.var.dim.split("x")
        self.target_area = TargetArea(self.var)

        # setting up layout
        self.grid_layout = QtWidgets.QGridLayout(self)
        self.layout2 = QtWidgets.QHBoxLayout(self)

        # self.layout2.addWidget(self.lefty, 2.5)
        self.layout2.addWidget(self.target_area, 5)
        self.layout2.addWidget(self.righty, 2.5)

        # adding layouts to grid
        self.grid_layout.addLayout(self.layout2, 0, 0)
        self.grid_layout.addWidget(self.bottom, 2, 0, 2, 1)

    @QtCore.Slot()
    def updateTarget(self):
        pass

    @QtCore.Slot()
    def gridSizeInDeg(self):
        pass


class TargetArea(QWidget):
    """
    Class for the grid display
    """

    def __init__(self, var):
        super().__init__()

        self.var = var
        self.config = configparser.ConfigParser()
        self.config.read(self.var.config_name)
        self.grid_size = self.config.get("test", "grid_size")
        self.circle_vis = self.config.get("test", "fixation_circle_visible")
        self.horz_lines = int(self.var.dim[0])
        self.vert_lines = int(self.var.dim[1])

    def paintEvent(self, arg__0):
        """
        This paints the grid with the lines and the size of it
        :param arg__0:
        :return:
        """

        painter = QPainter(self)
        painter.setBrush(QColor(75, 75, 75))
        painter.setRenderHint(QPainter.Antialiasing, True)

        rect = painter.window()

        # sets up the size of the circle based on the window size
        radii = np.minimum(rect.width(), rect.height()) / 2
        # win_h = rect.height() / 2
        # win_w = rect.width() / 2
        cent = QPoint(rect.width() / 2, rect.height() / 2)
        # sets up the size of the grid lines (will need to be changed to be custom size)
        if self.grid_size == 'small':
            num_of_lines = 31
        elif self.grid_size == 'medium':
            num_of_lines = 41
        elif self.grid_size == 'large':
            num_of_lines = 61
        else:
            num_of_lines = 0

        if self.horz_lines % 2 == 0:
            self.horz_lines += 1

        if self.vert_lines % 2 == 0:
            self.vert_lines += 1

        # spacing of lines
        spacing = (radii * 2) / num_of_lines
        # spacing_h = (win_h*2)/ self.horz_lines
        # spacing_v = (win_w*2)/ self.vert_lines
        # painter.drawRect(rect.width() / 2 - win_w, rect.height() / 2 - win_h, win_w * 2, win_h * 2)
        painter.drawRect(rect.width() / 2 - radii, rect.height() / 2 - radii, radii * 2, radii * 2)

        # Generating the steps for painting the lines in different colors
        horz_steps = np.linspace(rect.width() / 2 - radii, rect.width() / 2 + radii, self.horz_lines)
        vert_steps = np.linspace(rect.height() / 2 - radii, rect.height() / 2 + radii, self.vert_lines)

        center_line = (num_of_lines - 1) / 2
        # center_h = (self.horz_lines - 1) / 2
        # center_v = (self.vert_lines - 1) / 2

        # paints the lines with different colors depending on what step they are
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

        # used to set circle visible on  screen (from config file)
        if self.circle_vis == "1":
            painter.setPen(QPen(QColor(3, 175, 224), 2.5))
            painter.drawArc((rect.width() / 2) - (spacing * 15.25), (rect.height() / 2) - (spacing * 15.25),
                            spacing * 30.5, spacing * 30.5, 0, 16 * 360)
        else:
            pass
        painter.setPen(Qt.black)


# class TargetLefty(QWidget):
#     """
#     Class for the left panel of the window -- currently not being used
#     """
#
#     def __init__(self, eye, sub_id, save_loc, device, var):
#         super().__init__()
#
#         self.target = NuclearInfo(eye, sub_id, save_loc, device)
#
#         self.layout = QtWidgets.QHBoxLayout(self)
#         self.layout.addWidget(self.target)
#
#     def paintEvent(self, arg__0):
#         pass
#         # painter = QPainter(self)
#         # painter.setBrush(Qt.cyan)
#         # painter.setRenderHint(QPainter.Antialiasing, True)
#         #
#         # rect = painter.window()
#         #
#         # radii = np.minimum(rect.width(), rect.height())/2
#         # cent = QPoint(rect.width()/2, rect.height()/2)
#         #
#         # painter.drawEllipse(cent, radii, radii)


class TargetRighty(QWidget):
    """
    Class for the right panel of the window
    """

    def __init__(self, var):
        super().__init__()

        self.var = var
        # calls the control panel
        self.target = Tabs(self.var)

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
    """
    Class for the bottom panel of the window
    """

    def __init__(self, var):
        super().__init__()

        self.var = var
        # calls the notes panel
        self.target = NuclearNotes(self.var)

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
