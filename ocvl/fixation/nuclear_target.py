from PySide6 import QtGui
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt, QPoint, QPointF
from PySide6.QtGui import QScreen, QPainter, QColor, QPen, QPixmap, QBrush
import random


class NuclearTarget(QWidget):

    # maybe want to put this in the config file
    # The number of ppd of the screen we'll be projecting to (e.g. Lightcrafter, Projector, etc).
    SCREEN_PPD = 20

    def __init__(self, var):
        super().__init__()
        self.var = var
        display_monitor = 0
        #send it to a different monitor and make full screen
        monitors = QScreen.virtualSiblings(self.screen())
        monitor = monitors[display_monitor].availableGeometry()
        self.move(monitor.left(), monitor.top())
        self.showFullScreen()

        self.init = 1
        defaults = self.var.config.get("test", "fixation_default").split("/")

        if defaults[0] == 'on':
            self.var.target_vis = True
        else:
            self.var.target_vis = False
        self.var.custom_color = QtGui.QColor(defaults[1])
        self.var.size = int(defaults[2])
        self.var.shape = defaults[3]
        self.list1 = [1, 2, 3, 4]
        # self.rand_num = random.choice(self.list1)
        self.rand_num = 1
        # self.prev = 1
        self.count = 0
        self.var.center_x = QPainter(self).window().width() / 2
        self.var.center_y = QPainter(self).window().height() / 2



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

        # if GUI has checkbox checked for target visible
        if self.var.target_vis:
            # set color of target
            # need to set the pen and brush so there is no undesirable outline of the drawn items
            painter.setPen(self.var.custom_color)
            painter.setBrush(self.var.custom_color)

            if self.init == 1:
                # set it to the middle of the screen with this
                self.var.center_x = rect.width()/2
                self.var.center_y = rect.height()/2
                self.var.center_x_og = rect.width() / 2
                self.var.center_y_og = rect.height() / 2
                self.init = 0

            # updating the current target location
            self.var.center_x = self.var.center_x_og + self.var.x_val * self.var.screen_ppd
            self.var.center_y = self.var.center_y_og - self.var.y_val * self.var.screen_ppd

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
                    pen = QtGui.QPen(self.var.custom_color, self.var.size * 0.4)
                    painter.setPen(pen)
                    # draw the parts of the shape that always stay the same
                    painter.drawLine(self.var.center_x + (self.var.size*0.6), self.var.center_y, self.var.center_x - (self.var.size*0.6), self.var.center_y)
                    painter.drawLine(self.var.center_x, self.var.center_y + (self.var.size*0.6), self.var.center_x, self.var.center_y - (self.var.size*0.6))
                    painter.drawLine(self.var.center_x + self.var.size, self.var.center_y + self.var.size, self.var.center_x - self.var.size, self.var.center_y - self.var.size)
                    painter.drawLine(self.var.center_x - self.var.size, self.var.center_y + self.var.size, self.var.center_x + self.var.size, self.var.center_y - self.var.size)

                    # this is necessary so it doesn't change too fast
                    if self.count == 2:
                        if self.rand_num == 1:
                            self.rand_num = 2
                        elif self.rand_num == 2:
                            self.rand_num = 3
                        elif self.rand_num == 3:
                            self.rand_num = 4
                        elif self.rand_num == 4:
                            self.rand_num = 1
                        # self.rand_num = random.choice(self.list1)
                        # # while loop so that there are no numbers in a row.
                        # while self.rand_num == self.prev:
                        #     self.rand_num = random.choice(self.list1)
                        self.count = 0

                    # draw the parts of the shape that change (currently drawn or not)
                    match self.rand_num:
                        case 1:
                            painter.drawLine(self.var.center_x + (self.var.size*1.4), self.var.center_y, self.var.center_x + (self.var.size*1.4), self.var.center_y)
                        case 2:
                            painter.drawLine(self.var.center_x, self.var.center_y + (self.var.size * 1.4), self.var.center_x, self.var.center_y + (self.var.size * 1.4))
                        case 3:
                            painter.drawLine(self.var.center_x - (self.var.size * 1.4), self.var.center_y, self.var.center_x - (self.var.size * 1.4), self.var.center_y)
                        case 4:
                            painter.drawLine(self.var.center_x, self.var.center_y - (self.var.size*1.4), self.var.center_x, self.var.center_y - (self.var.size*1.4))

                    painter.setPen(self.var.custom_color)
                    # self.prev = self.rand_num
                    self.count = self.count + 1

        self.update()


