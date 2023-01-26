from PySide6 import QtWidgets, QtCore, QtQuick, QtGui
from PySide6.QtCore import QPoint, QRect
from PySide6.QtGui import QPainter, Qt, QPen, QColor, QPixmap
from PySide6.QtWidgets import QWidget, QLabel, QSizePolicy
import numpy as np
from ocvl.fixation.nuclear_controls import Tabs
from ocvl.fixation.nuclear_notes import NuclearNotes


class NuclearDisplay(QWidget):
    def __init__(self, var):
        super().__init__()

        self.var = var

        # setting up GUI panels
        self.righty = TargetRighty(self.var)
        self.bottom = TargetBottom(self.var)

        # Get the dims from the Configuration tabs
        var.dim = self.righty.target.var.dim.split("x")
        # may not be the best way to send instance - maybe save all instances as vars...
        self.target_area = TargetArea(self.var, self.righty)

        # setting up layout
        self.grid_layout = QtWidgets.QGridLayout(self)
        self.layout2 = QtWidgets.QHBoxLayout(self)
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

    def __init__(self, var, nuclear_display_ref):
        super().__init__()
        # policy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        # policy.setHeightForWidth(True)
        # self.setSizePolicy(policy)

        self.setMinimumSize(700, 700)

        self.var = var
        self.nuclear_display_ref = nuclear_display_ref

        # Set up labels; Anatomical view is default
        if self.var.eye == 'OS':
            self.var.label_or = False
        else:
            self.var.label_or = True

        self.grid_size = self.var.config.get("test", "grid_size")
        self.circle_vis = self.var.config.get("test", "fixation_circle_visible")
        self.horz_lines = int(self.var.dim[0])
        self.vert_lines = int(self.var.dim[1])
        self.rendered = True
        self.init = 1
        self.position = None

    # def heightForWidth(self, width):
    #     return width

    def labels(self):
        left_label = QLabel(self.var.left_label)
        right_label = QLabel(self.var.right_label)

    def mouseReleaseEvent(self, event):
        self.position = event.pos()


    def paintEvent(self, arg__0):
        """
        This paints the grid with the lines and the size of it
        :param position:
        :param arg__0:
        :return:
        """

        painter = QPainter(self)
        painter.setBrush(QColor(75, 75, 75))
        painter.setRenderHint(QPainter.Antialiasing, True)

        rect = painter.window()

        # sets up the size of the circle based on the window size
        radii = np.minimum(rect.width(), rect.height()) / 2

        # updating the original center location on the grid (esp. if the size changes)
        self.var.center_x_og_grid = rect.width() / 2
        self.var.center_y_og_grid = rect.height() / 2

        # updating the current location on the grid (accounts for the size changing as well)
        self.var.center_x_grid = self.var.center_x_og_grid + self.var.x_val * self.var.grid_mult
        self.var.center_y_grid = self.var.center_y_og_grid - self.var.y_val * self.var.grid_mult

        # updating the grid multiplier based on the size of the grid
        self.var.grid_mult = (radii / (self.horz_lines - 1)) * 2

        # setting the position to the place the mouse clicked
        if self.position:
            self.var.x_val = -(self.var.center_x_og_grid - self.position.x()) / self.var.grid_mult
            self.var.y_val = (self.var.center_y_og_grid - self.position.y()) / self.var.grid_mult
            # call to update the x and y text boxes
            self.nuclear_display_ref.target.updateCoordText()
            self.position = None


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
        painter.drawRect(rect.width() / 2 - radii, rect.height() / 2 - radii, radii * 2, radii * 2)
        if self.var.grid_vis:
            # Generating the steps for painting the lines in different colors
            horz_steps = np.linspace(rect.width() / 2 - radii, rect.width() / 2 + radii, self.horz_lines)
            vert_steps = np.linspace(rect.height() / 2 - radii, rect.height() / 2 + radii, self.vert_lines)

            center_line = (num_of_lines - 1) / 2

            # paints the lines with different colors depending on what step they are
            counter = 0
            for y in vert_steps:
                if counter % 5 == 0:
                    if counter == center_line:
                        # painter.setPen(QPen(QColor(255, 79, 0), 2.5))
                        painter.setPen(QPen(QColor(255, 79, 0)))
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
                        # painter.setPen(QPen(QColor(255, 79, 0), 2.5))
                        painter.setPen(QPen(QColor(255, 79, 0)))
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
        painter.setBrush(Qt.NoBrush)
        painter.setPen(Qt.green)
        tmp = self.var.current_fov.split(" ")
        h_fov = float(tmp[0])
        v_fov = float(tmp[2])
        painter.drawRect(self.var.center_x_grid - ((radii/self.horz_lines) * h_fov), self.var.center_y_grid - ((radii/self.vert_lines) * v_fov), ((radii/self.horz_lines) * h_fov) * 2, ((radii/self.vert_lines) * v_fov) * 2)
        painter.setBrush(QColor(75, 75, 75))
        painter.setPen(Qt.black)

        # https://stackoverflow.com/questions/24927869/how-to-save-qwidget-as-image-automatically
        if self.rendered:
            self.rendered = False
            pixmap = QPixmap(self.size())
            self.render(pixmap)
            pixmap.save("test.png", "PNG", -1)
            self.rendered = True

        self.update()



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
