import math
from enum import StrEnum, auto

from PySide6 import QtGui
from PySide6.QtWidgets import QGraphicsItem
from PySide6.QtCore import QRectF, QPointF, QPoint
from PySide6.QtGui import QColor, QPainterPath, QPen, QBrush, QPainter


class TargetTypes(StrEnum):
    MALTESE_CROSS = auto(),
    CROSSHAIR = auto(),
    BULLSEYE = auto()

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

        points = []
        for i in range(8):
            # Outer tip
            angle1 = math.radians(i * 45)
            # Inner notch (halfway between tips)
            angle2 = math.radians(i * 45 + 22.5)

            # Outer Radius
            points.append(QPointF(self.size * math.cos(angle1),
                                  self.size * math.sin(angle1)))
            # Inner Radius (roughly 1/3 of outer)
            points.append(QPointF((self.size * 0.4) * math.cos(angle2),
                                   (self.size * 0.4) * math.sin(angle2)))

        # Create the path
        self.path_to_draw.moveTo(points[0])
        for i in range(1, len(points)):
            self.path_to_draw.lineTo(points[i])
        self.path_to_draw.closeSubpath()

    def setSize(self, newsize):
        self.size = newsize
        self.path_to_draw = QPainterPath()

        points = []
        for i in range(8):
            # Outer tip
            angle1 = math.radians(i * 45)
            # Inner notch (halfway between tips)
            angle2 = math.radians(i * 45 + 22.5)

            # Outer Radius
            points.append(QPointF(self.size * math.cos(angle1),
                                  self.size * math.sin(angle1)))
            # Inner Radius (roughly 1/3 of outer)
            points.append(QPointF((self.size * 0.4) * math.cos(angle2),
                                   (self.size * 0.4) * math.sin(angle2)))

        # Create the path
        self.path_to_draw.moveTo(points[0])
        for i in range(1, len(points)):
            self.path_to_draw.lineTo(points[i])
        self.path_to_draw.closeSubpath()

    def boundingRect(self):
        return QRectF(-self.size/0.4, -self.size/0.4, self.size/0.4, self.size/0.4)

    def paint(self, painter, option, widget):
        painter.setRenderHint(QPainter.Antialiasing)
        pen = QtGui.QPen(self.color, self.thickness)
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
        self.path_to_draw.closeSubpath()

    def setSize(self, newsize):
        self.size = newsize
        self.path_to_draw = QPainterPath()

        self.path_to_draw = QPainterPath()

        self.path_to_draw.moveTo(0, -self.size/2)
        self.path_to_draw.lineTo(0, self.size/2)
        self.path_to_draw.moveTo(-self.size/2, 0)
        self.path_to_draw.lineTo(self.size/2, 0)
        self.path_to_draw.closeSubpath()

    def boundingRect(self):
        return QRectF(-self.size/2, -self.size/2, self.size/2, self.size/2)

    def paint(self, painter, option, widget):
        painter.setRenderHint(QPainter.Antialiasing)
        pen = QtGui.QPen(self.color, self.thickness)
        painter.setPen(pen)
        painter.drawPath(self.path_to_draw)


class BullsEye(Target):

    def __init__(self, size=5, thickness=1, color=QColor("white")):
        super().__init__(TargetTypes.BULLSEYE, size, thickness, color)

        self.path_to_draw = QPainterPath()

        self.path_to_draw.moveTo(0, 0)
        self.path_to_draw.addEllipse(-self.size/2, -self.size/2, self.size, self.size)
        self.path_to_draw.closeSubpath()

    def setSize(self, newsize):
        self.size = newsize
        self.path_to_draw = QPainterPath()

        self.path_to_draw.moveTo(0, 0)
        self.path_to_draw.addEllipse(-self.size/2, -self.size/2, self.size, self.size)
        self.path_to_draw.closeSubpath()

    def boundingRect(self):
        return QRectF(-self.size/2, -self.size/2, self.size/2, self.size/2)

    def paint(self, painter, option, widget):
        painter.setRenderHint(QPainter.Antialiasing)
        pen = QPen(self.color, self.thickness)
        brush = QBrush(self.color)
        painter.setPen(pen)
        painter.drawPath(self.path_to_draw)
        painter.setBrush(brush)
        painter.setPen(QPen())
        painter.drawEllipse(QPoint(), self.size/10, self.size/10)

class TargetFactory:
    _targets = {
        TargetTypes.CROSSHAIR: CrossHair,
        TargetTypes.MALTESE_CROSS: MalteseCross,
        TargetTypes.BULLSEYE: BullsEye
    }

    @staticmethod
    def get_target(target_type: TargetTypes, size: int = 5, thickness: float = 1.0, color: QColor = QColor("white")) -> Target:
        target_class = TargetFactory._targets.get(target_type)
        if target_class:
            return target_class(size, thickness, color)
        print(f"Unknown shape type: {target_type}, defaulting to bullseye.")
        return TargetFactory._targets.get(TargetTypes.BULLSEYE)(size, thickness, color)