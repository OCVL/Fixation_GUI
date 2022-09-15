import configparser
import math

from PySide6 import QtWidgets, QtCore
from PySide6.QtCore import QPoint, QRect
from PySide6.QtGui import QPainter, Qt, QPen, QColor
from PySide6.QtWidgets import QWidget, QDialog, QDialogButtonBox, QVBoxLayout, QLabel, QFormLayout, QLineEdit, \
    QPushButton, QHBoxLayout, QRadioButton, QComboBox
import numpy as np
from tkinter import filedialog


class NuclearDisplay(QWidget):
    def __init__(self):
        super().__init__()

        dlg = CustomDialog()
        dlg.exec()
        c_name = dlg.config_name
        self.target_area = TargetArea(c_name)
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

class CustomDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Setup")
        self.config = configparser.ConfigParser()
        self.config_name = filedialog.askopenfilenames(title='Select the configuration file', filetypes=[
            ("configuration file", ".ini")])
        self.config.read(self.config_name)
        self.device_list = self.config.get("ALL", "device_list").split("/")
        self.setup()

    def setup(self):
        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        layout1 = QFormLayout()
        eye_butt_layout = QHBoxLayout()
        save_loc_butt_layout = QHBoxLayout()

        self.save_location_butt = QPushButton("Save Location")
        left_eye = QRadioButton("OS")
        right_eye = QRadioButton("OD")

        left_eye.toggled.connect(self.eye_slot)
        right_eye.toggled.connect(self.eye_slot)

        self.sub_id = QLineEdit()
        self.sub_id.textChanged.connect(self.onTextEnter)

        self.device_menu = QComboBox()
        for x in self.device_list:
            self.device_menu.addItem(x)

        save_loc_butt_layout.addWidget(self.save_location_butt)
        eye_butt_layout.addWidget(left_eye)
        eye_butt_layout.addWidget(right_eye)

        layout1.addRow("Select Eye", eye_butt_layout)
        layout1.addRow("Subject ID:", self.sub_id)
        layout1.addRow("Select Save Location", save_loc_butt_layout)
        layout1.addRow(QLabel(""))
        layout1.addRow("Device", self.device_menu)
        layout1.addWidget(self.buttonBox)

        self.setLayout(layout1)

    def eye_slot(self):
        button = self.sender()
        if button.isChecked():
            print("Pressed the button called: " + button.text())

    def onTextEnter(self):
        print(self.sub_id.text())


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
