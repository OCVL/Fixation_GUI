from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt, QPoint
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

        match self.var.shape:
            case "Large Crosshair":
                # vertical line of crosshair
                painter.drawRect((rect.width() / 2), 0, 5, rect.height())
                # horizontal line of crosshair
                painter.drawRect(0, rect.height() / 2, rect.width(), 5)

            case "Small Crosshair":
                # vertical line of crosshair
                painter.drawRect((rect.width() / 2), (rect.height() / 2) -10, 5, 25)
                # horizontal line of crosshair
                painter.drawRect((rect.width() / 2) -10, (rect.height() / 2), 25, 5)

            case "Maltese Cross":
                # Will be changed to what each shape will look like in the future
                print("sierra mist is dead 2")
            case "Square Outline":
                # Will be changed to what each shape will look like in the future
                print("sierra mist is dead 3")
            case "Square":
                # Will be changed to what each shape will look like in the future
                print("sierra mist is dead 4")
            case "Circle":
                # Will be changed to what each shape will look like in the future
                print("sierra mist is dead 5")
            case "Twinkle":
                # Will be changed to what each shape will look like in the future
                print("sierra mist is dead 6")

        # # Large Crosshair
        # # vertical line of crosshair
        # painter.drawRect(rect.width()/2, 0, 5, rect.height())
        # # horizontal line of crosshair
        # painter.drawRect(0, rect.height() / 2, rect.width(), 5)

        self.update()


