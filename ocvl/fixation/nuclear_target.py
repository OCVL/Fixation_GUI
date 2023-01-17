from PySide6 import QtGui
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt, QPoint, QPointF
from PySide6.QtGui import QScreen, QPainter, QColor, QPen, QPixmap, QBrush
import numpy as np
import configparser


class NuclearTarget(QWidget):

    def __init__(self, var):
        super().__init__()
        self.var = var
        display_monitor = 1
        #send it to a different monitor and make full screen
        monitors = QScreen.virtualSiblings(self.screen())
        monitor = monitors[display_monitor].availableGeometry()
        self.move(monitor.left(), monitor.top())
        self.showFullScreen()

        self.config = configparser.ConfigParser()
        self.config.read(self.var.config_name)
        self.init = 1


    def paintEvent(self, arg__0):
        '''

        :param arg__0:
        :return:
        '''

        painter = QPainter(self)
        painter.setBrush(QColor(0, 0, 0))
        painter.setRenderHint(QPainter.Antialiasing, True)

        rect = painter.window()

        # filling the background with black
        painter.drawRect(0, 0, rect.width(), rect.height())

        # set color of target
        # need to set the pen and brush so there is no undesirable outline of the drawn items
        painter.setPen(self.var.custom_color)
        painter.setBrush(self.var.custom_color)

        if self.init == 1:
            # set it to the middle of the screen with this
            self.var.center_x = rect.width()/2
            self.var.center_y = rect.height()/2
            self.init = 0

        match self.var.shape:
            case "Large Crosshair":
                # vertical line of crosshair
                painter.drawRect(self.var.center_x-(self.var.size/2), 0, self.var.size, rect.height())
                # horizontal line of crosshair
                painter.drawRect(0, self.var.center_y-(self.var.size/2), rect.width(), self.var.size)

            case "Small Crosshair":
                # vertical line of crosshair
                painter.drawRect(self.var.center_x-(self.var.size/2), self.var.center_y - ((self.var.size * 5)/2), self.var.size, self.var.size * 5)
                # horizontal line of crosshair
                painter.drawRect(self.var.center_x - ((self.var.size * 5)/2), self.var.center_y-(self.var.size/2), self.var.size * 5, self.var.size)

            case "Maltese Cross":
                pen = QtGui.QPen(self.var.custom_color, self.var.size*0.35)
                painter.setPen(pen)
                painter.drawLine(self.var.center_x+(self.var.size*0.8), self.var.center_y+(self.var.size*1.6), self.var.center_x-(self.var.size*0.8), self.var.center_y-(self.var.size*1.6))
                painter.drawLine(self.var.center_x-(self.var.size*0.8), self.var.center_y+(self.var.size*1.6), self.var.center_x+(self.var.size*0.8), self.var.center_y-(self.var.size*1.6))
                painter.drawLine(self.var.center_x+(self.var.size*1.6), self.var.center_y+(self.var.size*0.8), self.var.center_x-(self.var.size*1.6), self.var.center_y-(self.var.size*0.8))
                painter.drawLine(self.var.center_x+(self.var.size*1.6), self.var.center_y-(self.var.size*0.8), self.var.center_x-(self.var.size*1.6), self.var.center_y+(self.var.size*0.8))
                painter.drawLine(self.var.center_x, self.var.center_y+self.var.size, self.var.center_x+(self.var.size*0.8), self.var.center_y+(self.var.size*1.6))
                painter.drawLine(self.var.center_x, self.var.center_y+self.var.size, self.var.center_x-(self.var.size*0.8), self.var.center_y+(self.var.size*1.6))
                painter.drawLine(self.var.center_x, self.var.center_y-self.var.size, self.var.center_x+(self.var.size*0.8), self.var.center_y-(self.var.size*1.6))
                painter.drawLine(self.var.center_x, self.var.center_y-self.var.size, self.var.center_x-(self.var.size*0.8), self.var.center_y-(self.var.size*1.6))
                painter.drawLine(self.var.center_x+self.var.size, self.var.center_y, self.var.center_x+(self.var.size*1.6), self.var.center_y-(self.var.size*0.8))
                painter.drawLine(self.var.center_x+self.var.size, self.var.center_y, self.var.center_x+(self.var.size*1.6), self.var.center_y+(self.var.size*0.8))
                painter.drawLine(self.var.center_x-self.var.size, self.var.center_y, self.var.center_x-(self.var.size*1.6), self.var.center_y-(self.var.size*0.8))
                painter.drawLine(self.var.center_x-self.var.size, self.var.center_y, self.var.center_x-(self.var.size*1.6), self.var.center_y+(self.var.size*0.8))
                painter.setPen(self.var.custom_color)
            case "Square":
                painter.drawRect(self.var.center_x - self.var.size, self.var.center_y - self.var.size, self.var.size * 2, self.var.size * 2)
            case "Circle":
                center = QPointF(self.var.center_x, self.var.center_y)
                painter.drawEllipse(center, self.var.size, self.var.size)
            case "Twinkle":
                # Will be changed to what each shape will look like in the future
                print("sierra mist is dead")

        self.update()


