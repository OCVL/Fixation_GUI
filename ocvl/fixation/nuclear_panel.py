from datetime import datetime
import pandas
from PySide6 import QtWidgets, QtCore, QtQuick, QtGui
from PySide6.QtCore import QPoint, QRect
from PySide6.QtGui import QPainter, Qt, QPen, QColor, QPixmap, QImage
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
        self.var.control_ref = self.righty
        self.bottom = TargetBottom(self.var)
        self.var.notes_ref = self.bottom

        # Get the dims from the Configuration tabs
        self.var.dim = self.var.dim.split("x")
        self.target_area = TargetArea(self.var)

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

    def __init__(self, var):
        super().__init__()
        # policy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        # policy.setHeightForWidth(True)
        # self.setSizePolicy(policy)

        self.setMinimumSize(700, 700)

        self.var = var

        # Set up label text
        if self.var.eye == 'OS':
            self.var.left_label = "Nasal"
            self.var.right_label = "Temporal"
        else:
            self.var.left_label = "Temporal"
            self.var.right_label = "Nasal"

        self.grid_size = self.var.config.get("test", "grid_size")
        self.circle_vis = self.var.config.get("test", "fixation_circle_visible")
        self.horz_lines = int(self.var.dim[0])
        self.vert_lines = int(self.var.dim[1])
        self.rendered = True
        self.init = 1
        self.position = None
        self.prev_vid_num = -1
        self.video_list = pandas.DataFrame(columns=["Video Number", "Location", "FOV"])

        # getting the name of the device from the config file
        device_name = self.var.config.get("test", "device")
        # getting the base for the saving/naming conventions for the files
        self.grid_name = (self.var.save_loc + '/' + self.var.sub_id + '_' + datetime.today().strftime(
            '%Y%m%d') + '_' + self.var.eye + '_' + device_name + '_' + 'Grid.png')

        # self.video_list.columns =

    # def heightForWidth(self, width):
    #     return width

    def mouseReleaseEvent(self, event):
        self.position = event.pos()


    def paintEvent(self, arg__0):
        """
        This paints the grid with the lines and the size of it
        :param position:
        :param arg__0:
        :return:
        """



        # need to get the number of horz and vert lines each time in case the dimensions have changed
        self.horz_lines = int(self.var.dim[0])
        self.vert_lines = int(self.var.dim[1])

        tmp = self.var.current_fov.split(" ")
        h_fov = float(tmp[0])
        v_fov = float(tmp[2])

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
        if self.var.ref_point:
            self.var.center_x_grid = self.var.center_x_og_grid + (self.var.x_val - self.var.x_ref) * self.var.grid_mult
            self.var.center_y_grid = self.var.center_y_og_grid - (self.var.y_val - self.var.y_ref) * self.var.grid_mult
        else:
            self.var.center_x_grid = self.var.center_x_og_grid + self.var.x_val * self.var.grid_mult
            self.var.center_y_grid = self.var.center_y_og_grid - self.var.y_val * self.var.grid_mult

        # updating the grid multiplier based on the size of the grid
        self.var.grid_mult = (radii / self.horz_lines) * 2

        # setting the position to the place the mouse clicked
        if self.position:
            self.var.x_val = -(self.var.center_x_og_grid - self.position.x()) / self.var.grid_mult
            self.var.y_val = (self.var.center_y_og_grid - self.position.y()) / self.var.grid_mult
            # call to update the x and y text boxes
            self.var.control_ref.target.updateCoordText()
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

        # adds video list entry to pandas dataframe video list to keep track of taken videos
        if self.var.video_list_entry:
            if self.var.video_list_entry[0] != self.prev_vid_num:
                self.video_list.loc[len(self.video_list.index)] = self.var.video_list_entry
                self.prev_vid_num = self.var.video_list_entry[0]

        # paints all the FOVs at the correct locations for all the videos in the video list
        for index, row in self.video_list.iterrows():
            # parse the location
            locs = row['Location']
            locs2 = locs.split(",")
            locs3 = locs2[0].split("(")
            locs4 = locs2[1].split(")")
            x_loc = float(locs3[1])
            y_loc = float(locs4[0])
            x_loc = self.var.center_x_og_grid + x_loc * self.var.grid_mult
            y_loc = self.var.center_y_og_grid - y_loc * self.var.grid_mult

            # parse the FOV
            fov = row['FOV']
            fov2 = fov.split(" ")
            x_fov = float(fov2[0])
            y_fov = float(fov2[2])

            # paint the recorded video locations with the correct FOV
            painter.setBrush(Qt.NoBrush)
            painter.setPen(QColor(0, 206, 207))
            painter.drawRect(x_loc - ((radii / self.horz_lines) * x_fov),
                             y_loc - ((radii / self.vert_lines) * y_fov),
                             ((radii / self.horz_lines) * x_fov) * 2, ((radii / self.vert_lines) * y_fov) * 2)
            painter.setBrush(QColor(75, 75, 75))
            painter.setPen(Qt.black)

        if self.var.image_path is not None:
            # pxmp = QPixmap().loadFromData(self.var.image_path)
            # painter.drawPixmap(rect, pxmp)
            painter.drawImage(QRect(100, 50, 100, 100), QImage(self.var.image_path))

        # used to set circle visible on  screen (from config file)
        if self.circle_vis == "1":
            painter.setPen(QPen(QColor(3, 175, 224), 2.5))
            painter.drawArc((rect.width() / 2) - (spacing * 15.25), (rect.height() / 2) - (spacing * 15.25),
                            spacing * 30.5, spacing * 30.5, 0, 16 * 360)
        else:
            pass
        painter.setBrush(Qt.NoBrush)
        painter.setPen(Qt.green)
        # second 2 are the size
        painter.drawRect(self.var.center_x_grid - ((radii/self.horz_lines) * h_fov), self.var.center_y_grid - ((radii/self.vert_lines) * v_fov), ((radii/self.horz_lines) * h_fov) * 2, ((radii/self.vert_lines) * v_fov) * 2)
        painter.setBrush(QColor(75, 75, 75))
        painter.setPen(Qt.black)

        # https://stackoverflow.com/questions/24927869/how-to-save-qwidget-as-image-automatically
        if self.rendered:
            self.rendered = False
            pixmap = QPixmap(self.size())
            self.render(pixmap)
            pixmap.save(self.grid_name, "PNG", -1)
            self.rendered = True

        painter.setPen(Qt.white)
        font = QtGui.QFont()
        font.setPointSize(10)
        painter.setFont(font)
        painter.drawText((rect.width() / 2)-22, 10, 'Superior')
        painter.drawText((rect.width() / 2)-22, (radii * 2) - 2, 'Inferior')
        # painter.drawText(rect.width() / 2 - radii, (rect.height() / 2) -20, "N")
        # painter.drawText(rect.width() / 2 - radii, (rect.height() / 2) -10, "a")
        # painter.drawText(rect.width() / 2 - radii, (rect.height() / 2), "s")
        # painter.drawText(rect.width() / 2 - radii, (rect.height() / 2) +10, "a")
        # painter.drawText(rect.width() / 2 - radii, (rect.height() / 2) +20, "l")
        # rect.width() / 2 - radii, rect.height() / 2 - radii, radii * 2, radii * 2
        painter.rotate(90)
        painter.drawText((rect.height() / 2)-20, -((rect.width() / 2)+ radii - 10), self.var.right_label)
        painter.rotate(-90)
        painter.rotate(-90)
        painter.drawText(-((rect.height() / 2)+20), ((rect.width() / 2)- radii + 10), self.var.left_label)
        painter.rotate(90)
        painter.setPen(Qt.black)



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
