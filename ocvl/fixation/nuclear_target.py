from enum import StrEnum

from PySide6 import QtGui
from PySide6.QtWidgets import  QGraphicsItem, QGraphicsScene, QGraphicsView
from PySide6.QtCore import QRectF, QLineF
from PySide6.QtGui import QScreen, QPainter, QColor, QPainterPath

class TargetTypes(StrEnum):
    MALTESE_CROSS = "Maltese Cross",
    CROSSHAIR = "Crosshair",
    BULLSEYE = "Bullseye"

class Target(QGraphicsItem):
    def __init__(self, name, size=5, thickness=1, color=QColor("white")):
        super().__init__()
        self._name = name
        self.size = size
        self.thickness = thickness
        self.color = color

    def setColor(self, color):
        self.color = color

    def setThickness(self, thickness):
        self.thickness = thickness

    def setSize(self, newsize):
        self.size = newsize

    def getName(self):
        return self._name


class MalteseCross(Target):
    def __init__(self, size=5, thickness=1, color=QColor("white")):
        super().__init__(TargetTypes.MALTESE_CROSS, size, thickness, color)

        self.path_to_draw = QPainterPath()

        self.path_to_draw.moveTo(-self.size * 0.8, self.size * 1.6)
        self.path_to_draw.lineTo(self.size * 0.8, self.size * 1.6)
        self.path_to_draw.moveTo(-self.size * 0.8, self.size * 1.6)
        self.path_to_draw.lineTo(self.size * 0.8, -self.size * 1.6)
        self.path_to_draw.moveTo(self.size * 1.6, self.size * 0.8)
        self.path_to_draw.lineTo(-self.size * 1.6, -self.size * 0.8)
        self.path_to_draw.moveTo(self.size * 1.6, -self.size * 0.8)
        self.path_to_draw.lineTo(-self.size * 1.6, self.size * 0.8)
        self.path_to_draw.moveTo(0, self.size)
        self.path_to_draw.lineTo(self.size * 0.8, self.size * 1.6),
        self.path_to_draw.moveTo(0, self.size)
        self.path_to_draw.lineTo(-self.size * 0.8, self.size * 1.6)
        self.path_to_draw.moveTo(0, -self.size)
        self.path_to_draw.lineTo(self.size * 0.8, -self.size * 1.6)
        self.path_to_draw.moveTo(0, -self.size)
        self.path_to_draw.lineTo(-self.size * 0.8, -self.size * 1.6)
        self.path_to_draw.moveTo(0, self.size)
        self.path_to_draw.lineTo(self.size * 1.6, -self.size * 0.8),
        self.path_to_draw.moveTo(0, self.size)
        self.path_to_draw.lineTo(self.size * 1.6, self.size * 0.8),
        self.path_to_draw.moveTo(0, -self.size)
        self.path_to_draw.lineTo(-self.size * 1.6, -self.size * 0.8)
        self.path_to_draw.moveTo(0, -self.size)
        self.path_to_draw.lineTo(-self.size * 1.6, self.size * 0.8)

    def setSize(self, newsize):
        self.size = newsize
        self.path_to_draw = QPainterPath()

        self.path_to_draw.moveTo(-self.size * 0.8, self.size * 1.6)
        self.path_to_draw.lineTo(self.size * 0.8,  self.size * 1.6)
        self.path_to_draw.moveTo(-self.size * 0.8,  self.size * 1.6)
        self.path_to_draw.lineTo( self.size * 0.8,  -self.size * 1.6)
        self.path_to_draw.moveTo( self.size * 1.6,  self.size * 0.8)
        self.path_to_draw.lineTo( -self.size * 1.6,  -self.size * 0.8)
        self.path_to_draw.moveTo( self.size * 1.6,  -self.size * 0.8)
        self.path_to_draw.lineTo( -self.size * 1.6,  self.size * 0.8)
        self.path_to_draw.moveTo( 0, self.size)
        self.path_to_draw.lineTo( self.size * 0.8, self.size * 1.6),
        self.path_to_draw.moveTo( 0, self.size)
        self.path_to_draw.lineTo( -self.size * 0.8, self.size * 1.6)
        self.path_to_draw.moveTo( 0, -self.size)
        self.path_to_draw.lineTo( self.size * 0.8, -self.size * 1.6)
        self.path_to_draw.moveTo( 0, -self.size)
        self.path_to_draw.lineTo( -self.size * 0.8, -self.size * 1.6)
        self.path_to_draw.moveTo( 0, self.size)
        self.path_to_draw.lineTo(self.size * 1.6, -self.size * 0.8),
        self.path_to_draw.moveTo( 0, self.size)
        self.path_to_draw.lineTo(self.size * 1.6, self.size * 0.8),
        self.path_to_draw.moveTo( 0, -self.size)
        self.path_to_draw.lineTo(-self.size * 1.6, -self.size * 0.8)
        self.path_to_draw.moveTo( 0, -self.size)
        self.path_to_draw.lineTo( -self.size * 1.6, self.size * 0.8)

    def boundingRect(self):
        return QRectF(-self.size * 1.6, -self.size * 1.6, self.size * 1.6, self.size * 1.6)

    def paint(self, painter, option, widget):
        pen = QtGui.QPen(self.color, self.thickness * 0.35)
        painter.setPen(pen)
        painter.drawPath(self.path_to_draw)


class CrossHair(Target):

    def __init__(self, size=5, thickness=1, color=QColor("white")):
        super().__init__(TargetTypes.CROSSHAIR, size, thickness, color)

        self.path_to_draw = QPainterPath()

        self.path_to_draw.moveTo(0, -self.size/2)
        self.path_to_draw.lineTo(0, self.size/2)
        self.path_to_draw.moveTo(-self.size/2, 0)
        self.path_to_draw.lineTo(self.size/2, 0)

    def setSize(self, newsize):
        self.size = newsize
        self.path_to_draw = QPainterPath()

        self.path_to_draw = QPainterPath()

        self.path_to_draw.moveTo(0, -self.size/2)
        self.path_to_draw.lineTo(0, self.size/2)
        self.path_to_draw.moveTo(-self.size/2, 0)
        self.path_to_draw.lineTo(self.size/2, 0)

    def boundingRect(self):
        return QRectF(-self.size/2, -self.size/2, self.size/2, self.size/2)

    def paint(self, painter, option, widget):
        pen = QtGui.QPen(self.color, self.thickness * 0.35)
        painter.setPen(pen)
        painter.drawPath(self.path_to_draw)


class NuclearTarget(QGraphicsView):

    # maybe want to put this in the config file
    # The number of ppd of the screen we'll be projecting to (e.g. Lightcrafter, Projector, etc).
    SCREEN_PPD = 20

    def __init__(self, var):
        super().__init__()

        self.scene = QGraphicsScene()

        self.setScene(self.scene)

        self.var = var
        display_monitor = 0
        #send it to a different monitor and make full screen
        monitors = QScreen.virtualSiblings(self.screen())
        monitor = monitors[display_monitor].availableGeometry()
        self.move(monitor.left(), monitor.top())

        self.init = 1
        defaults = self.var.config.get("test", "fixation_default").split("/")

        if defaults[0] == 'on':
            self.var.target_vis = True
        else:
            self.var.target_vis = False

        self.var.center_x = QPainter(self).window().width() / 2
        self.var.center_y = QPainter(self).window().height() / 2

        self.targets = [CrossHair(size=self.var.size, thickness=self.var.thickness, color=self.var.custom_color),
                        MalteseCross(size=self.var.size, thickness=self.var.thickness, color=self.var.custom_color)]

        self.current_shape = None
        self.setTarget(self.var.shape)
        self.setFrameStyle(0)

    def setTarget(self, target_name) -> Target:

        self.scene.removeItem(self.current_shape)

        for target in self.targets:
            if target_name == target.getName():
                self.current_shape = target
                self.scene.addItem(target)

                return target

        return CrossHair()
