import sys
from datetime import datetime
import pandas
from PySide6 import QtWidgets, QtCore, QtQuick, QtGui
from PySide6.QtCore import QPoint, QRect, QLineF
from PySide6.QtGui import QPainter, Qt, QPen, QColor, QPixmap, QImage, QTransform, QBrush, QFont
from PySide6.QtWidgets import QWidget, QLabel, QSizePolicy, QGraphicsView, QGraphicsScene, QVBoxLayout, \
    QGraphicsItemGroup, QGraphicsLineItem
import numpy as np
from ocvl.fixation.participant_display import ParticipantDisplay


class FixationDisplay(QWidget):
    def __init__(self, config=None):
        super(FixationDisplay, self).__init__()

        if config is None:
            config = dict()

        self.op_disp_config = config.get("operator_display", dict())

        # self.participant_display = ParticipantDisplay(config.get("participant_display", dict()))
        # self.participant_display.show()

        self.layout = QVBoxLayout(self)

        # Get the dims from the Configuration tabs
        self.target_area = _OperatorDisplay(self.op_disp_config)

        self.layout.addWidget(self.target_area)


    @QtCore.Slot()
    def updateTarget(self):
        pass

    @QtCore.Slot()
    def gridSizeInDeg(self):
        pass


class _OperatorDisplay(QGraphicsView):
    """
    Class for the grid display
    """

    def __init__(self, config):
        super(_OperatorDisplay, self).__init__()

        self.op_config = config

        self.width = self.op_config.get("width_in_px", 600)
        self.height = self.op_config.get("height_in_px", 600)
        self.center_x = self.width / 2
        self.center_y = self.height / 2
        self.ppd = self.op_config.get("ppd", 20)

        self.setMinimumSize(self.width, self.height)
        self.scene = QGraphicsScene(0, 0, self.width, self.height, self)
        self.setScene(self.scene)

        self.left_label = "Temporal"
        self.right_label = "Nasal"

        # Accepts anything described in https://doc.qt.io/qt-6/qcolor.html#fromString
        bkgrd_color = QColor.fromString(str(self.op_config.get("background_color", "dimgray")))
        self.scene.addRect(0, 0, self.width, self.height,
                           QPen(), QBrush(bkgrd_color))

        # Make static items that are all centered in the operator display
        self.static_items = QGraphicsItemGroup()

        minor_color = QColor.fromString(str(self.op_config.get("minor_color", "lightgray")))
        minor_grid_pen = QPen(QBrush(minor_color), 1)
        if self.op_config.get("major_color") is not None:
            major_color = QColor.fromString(str(self.op_config.get("major_color", "whitesmoke")))
            major_grid_pen = QPen(QBrush(major_color), 3)
        else:
            major_grid_pen = None

        # Make vertical lines
        for v in np.arange(0.0, self.width/2.0, self.ppd, dtype=np.float32):
            liner = QGraphicsLineItem(v, -self.height / 2.0, v, self.height / 2.0)
            # Is a major line
            if (v/self.ppd) % 5 == 0 and major_grid_pen is not None:
                liner.setPen(major_grid_pen)
            else:
                liner.setPen(minor_grid_pen)
            self.static_items.addToGroup(liner)

        for v in np.arange(-self.ppd, -self.width/2.0, -self.ppd, dtype=np.float32):
            liner = QGraphicsLineItem(v, -self.height / 2.0, v, self.height / 2.0)
            # Is a major line
            if (v/-self.ppd) % 5 == 0 and major_grid_pen is not None:
                liner.setPen(major_grid_pen)
            else:
                liner.setPen(minor_grid_pen)
            self.static_items.addToGroup(liner)

        # Make horizontal lines
        for h in np.arange(0.0, self.height/2.0, self.ppd, dtype=np.float32):
            liner = QGraphicsLineItem(-self.width / 2.0, h, self.width / 2.0, h)
            # Is a major line
            if (h/self.ppd) % 5 == 0 and major_grid_pen is not None:
                liner.setPen(major_grid_pen)
            else:
                liner.setPen(minor_grid_pen)
            self.static_items.addToGroup(liner)

        for h in np.arange(-self.ppd, -self.height/2.0, -self.ppd, dtype=np.float32):
            liner = QGraphicsLineItem(-self.width / 2.0, h, self.width / 2.0, h)
            # Is a major line
            if (h/-self.ppd) % 5 == 0 and major_grid_pen is not None:
                liner.setPen(major_grid_pen)
            else:
                liner.setPen(minor_grid_pen)
            self.static_items.addToGroup(liner)

        self.static_items.setTransform(QTransform.fromTranslate(self.center_x, self.center_y))
        self.scene.addItem(self.static_items)

        # Make labels
        bkgrd_opposite = QColor(255-bkgrd_color.red(), 255-bkgrd_color.green(), 255-bkgrd_color.blue(), bkgrd_color.alpha())
        top_label = self.scene.addText("Superior", QFont("Arial", 12, QFont.Weight.Bold))
        top_label.setDefaultTextColor(bkgrd_opposite)
        top_label.setTransform(QTransform.fromTranslate(self.width / 2.0, 0))

        bottom_label = self.scene.addText("Inferior", QFont("Arial", 12, QFont.Weight.Bold))
        bottom_label.setDefaultTextColor(bkgrd_opposite)
        bottom_label.setTransform(QTransform.fromTranslate(self.width / 2.0, self.height - bottom_label.boundingRect().height() ))


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = FixationDisplay()
    widget.show()

    sys.exit(app.exec())
