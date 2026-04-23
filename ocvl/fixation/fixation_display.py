import sys
from PySide6 import QtWidgets
from PySide6.QtCore import QRectF, Slot, QPointF, QSize, QSizeF, Property, Signal
from PySide6.QtGui import QPen, QColor, QTransform, QBrush, QFont, QMouseEvent
from PySide6.QtWidgets import QWidget, QGraphicsView, QGraphicsScene, QVBoxLayout, \
    QGraphicsItemGroup, QGraphicsLineItem
import numpy as np

from ocvl.fixation.constants import Eye
from ocvl.fixation.participant_display import ParticipantDisplay
from ocvl.fixation.targets import Target


class FixationDisplay(QWidget):

    positionChanged = Signal(QPointF)

    def __init__(self, config: dict = None, parent: QWidget = None):
        super().__init__(parent)

        if config is None:
            config = dict()

        self.op_disp_config = config.get("operator_display", dict())

        self._participant_display = ParticipantDisplay(config.get("participant_display", dict()))
        self._participant_display.show()

        self.layout = QVBoxLayout(self)

        # Get the dims from the Configuration tabs
        self.operator_display = _OperatorDisplay(self.op_disp_config, self, mouse_enabled=config.get("allow_mouse_movement", False))

        self.layout.addWidget(self.operator_display)

        self.fov = QSize(1, 1)
        self.eye = Eye.OS
        self._target_position = QPointF(0, 0)


    #
    # class MyObject(QObject):
    #     def __init__(self):
    #         super().__init__()
    #         self._name = "Default"
    #
    #     def get_name(self):
    #         return self._name
    #
    #     def set_name(self, value):
    #         self._name = value
    #
    #     # Define a bindable property
    #     name = Property(str, get_name, set_name, bindable=True)
    #
    # # Usage
    # obj = MyObject()
    # bindable_name = QBindable(obj, "name")
    # bindable_name.setBinding(lambda: "Bound Value")
    # print(obj.name)  # Output: Bound Value
    #

    @Property(QPointF, notify=positionChanged)
    def target_position(self):
        return self._target_position

    @target_position.setter
    def target_position(self, position: QPointF):
        # In degrees of visual angle.
        self._target_position = position

        self.operator_display.imaging_rect.\
            setTransform(QTransform.fromTranslate(self.operator_display.center.x() + self._target_position.x() * self.operator_display.ppd,
                                                  self.operator_display.center.y() - self._target_position.y() * self.operator_display.ppd))

        self._participant_display.setPosition(self._target_position)

        self.positionChanged.emit(position)

    def getFOV(self):
        return self.fov

    @Slot()
    def onTargetChange(self, target: Target):
        self._participant_display.setTarget(target)

    @Slot()
    def onEyeChanged(self, new_eye: Eye):
        self.eye = new_eye
        if self.eye == Eye.OS:
            self.operator_display.left_label.setPlainText("Temporal")
            self.operator_display.right_label.setPlainText("Nasal")
        else:
            self.operator_display.left_label.setPlainText("Nasal")
            self.operator_display.right_label.setPlainText("Temporal")

    @Slot()
    def onFOVChanged(self, new_size: QSizeF):
        self.fov = new_size
        self.operator_display.imaging_rect.setRect((-self.fov.width() / 2.0) * self.operator_display.ppd,
                                                   (-self.fov.height() / 2.0) * self.operator_display.ppd,
                                                   self.fov.width() * self.operator_display.ppd,
                                                   self.fov.height() * self.operator_display.ppd)

    @Slot()
    def setPositionAsCenter(self):
        self.target_position = QPointF(0, 0)
        self.operator_display.imaging_rect.\
            setTransform(QTransform.fromTranslate(self.operator_display.center.x() + self._target_position.x() * self.operator_display.ppd,
                                                  self.operator_display.center.y() - self._target_position.y() * self.operator_display.ppd))

        self._participant_display.setCenter(self._participant_display.target_position)


class _OperatorDisplay(QGraphicsView):
    """
    Class for the grid display
    """

    def __init__(self, config: dict = None, parent: QWidget = None, mouse_enabled: bool = False):
        super().__init__(parent)

        self.mouse_pressed = False
        self.mouse_enabled = mouse_enabled
        if mouse_enabled:
            self.setMouseTracking(True)
        else:
            self.setMouseTracking(False)

        if config is None:
            self.config = dict()
        else:
            self.op_config = config

        self.width = self.op_config.get("width_in_px", 600)
        self.height = self.op_config.get("height_in_px", 600)
        self.center = QPointF(self.width / 2, self.height / 2)
        self.ppd = self.op_config.get("ppd", 20)

        self.setMinimumSize(self.width, self.height)
        self.scene = QGraphicsScene(0, 0, self.width, self.height, self)
        self.setScene(self.scene)

        # Accepts anything described in https://doc.qt.io/qt-6/qcolor.html#fromString
        bkgrd_color = QColor.fromString(str(self.op_config.get("background_color", "dimgray")))
        self.scene.addRect(0, 0, self.width, self.height,
                           QPen(), QBrush(bkgrd_color))

        # Make static items that are all centered in the operator display
        self.static_items = QGraphicsItemGroup()

        minor_color = QColor.fromString(str(self.op_config.get("minor_color", "black")))
        minor_grid_pen = QPen(QBrush(minor_color), 1)
        if self.op_config.get("major_color", "chocolate") is not None:
            major_color = QColor.fromString(str(self.op_config.get("major_color", "chocolate")))
            major_grid_pen = QPen(QBrush(major_color), 2)
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

        self.static_items.setTransform(QTransform.fromTranslate(self.center.x(), self.center.y()))
        self.scene.addItem(self.static_items)

        # Make axis labels
        top_label = self.scene.addText("Superior", QFont("Arial", 12, QFont.Weight.Bold))
        top_label.setDefaultTextColor(QColor.fromString(str(self.op_config.get("label_color", "whitesmoke"))))
        top_label.setTransform(QTransform.fromTranslate(self.width / 2.0 - top_label.boundingRect().width()/2, 0))

        bottom_label = self.scene.addText("Inferior", QFont("Arial", 12, QFont.Weight.Bold))
        bottom_label.setDefaultTextColor(QColor.fromString(str(self.op_config.get("label_color", "whitesmoke"))))
        bottom_label.setTransform(QTransform.fromTranslate((self.width / 2.0) - bottom_label.boundingRect().width()/2,
                                                            self.height - bottom_label.boundingRect().height()))

        self.left_label = self.scene.addText("Temporal", QFont("Arial", 12, QFont.Weight.Bold))
        self.left_label.setDefaultTextColor(QColor.fromString(str(self.op_config.get("label_color", "whitesmoke"))))
        self.left_label.setTransform(QTransform.fromTranslate(0, self.height / 2.0 - self.left_label.boundingRect().height()/2))

        self.right_label = self.scene.addText("Nasal", QFont("Arial", 12, QFont.Weight.Bold))
        self.right_label.setDefaultTextColor(QColor.fromString(str(self.op_config.get("label_color", "whitesmoke"))))
        self.right_label.setTransform(QTransform.fromTranslate(self.width - self.right_label.boundingRect().width(),
                                                               self.height / 2.0 - self.right_label.boundingRect().height()/2))

        # Make our imaging FOV rectangle
        self.imaging_rect = self.scene.addRect(QRectF(-self.ppd/2, -self.ppd/2, self.ppd, self.ppd))
        self.imaging_rect.setPen(QPen(QBrush(QColor.fromString(str(self.op_config.get("raster_color", "dodgerblue")))), 3))
        self.imaging_rect.setTransform(QTransform.fromTranslate(self.center.x(), self.center.y()))

    def mousePressEvent(self, event: QMouseEvent, /):
        self.mouse_pressed = True

    def mouseMoveEvent(self, event: QMouseEvent, /):
        if self.mouse_enabled and self.mouse_pressed:
            newpos = QPointF( event.position().x() - self.center.x(), self.center.y() - event.position().y())
            self.parentWidget().onPositionChanged( newpos / self.ppd )


    def mouseReleaseEvent(self, event: QMouseEvent, /):
        self.mouse_pressed = False
        if self.mouse_enabled:
            newpos = QPointF( event.position().x() - self.center.x(), self.center.y() - event.position().y())
            self.parentWidget().onPositionChanged( newpos / self.ppd )



if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = FixationDisplay()
    widget.show()

    sys.exit(app.exec())
