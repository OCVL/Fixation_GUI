
from PySide6.QtWidgets import QGraphicsScene, QGraphicsView
from PySide6.QtGui import QScreen, QTransform

from ocvl.fixation.targets import *


class ParticipantDisplay(QGraphicsView):

    def __init__(self, config, parent=None):
        super(ParticipantDisplay, self).__init__(parent)

        self.scene = QGraphicsScene(0, 0, 800, 800, self)

        self.setScene(self.scene)
        self.setMaximumSize(800, 800)
        self.setMinimumSize(800, 800)

        self.config = config
        display_monitor = 0
        #send it to a different monitor and make full screen
        monitors = QScreen.virtualSiblings(self.screen())
        monitor = monitors[display_monitor].availableGeometry()
        self.move(monitor.left(), monitor.top())

        self.init = 1

        self.center = self.center_x_og

        self.current_target = self.target_shape
        self.current_target.setTransform(QTransform.fromTranslate(self.config.target_center_x, self.config.target_center_y))
        self.scene.addItem(self.current_target)

        # self.shapeChanged.connect(self.setTarget)
        # self.xChanged.connect(self.updateTransform)
        # self.yChanged.connect(self.updateTransform)

        self.setFrameStyle(0)
        self.viewport().update()

    def setTarget(self, target: Target):
        self.scene.clear()
        self.viewport().update()

        self.current_target = target

        offset = QTransform.fromTranslate(self.target_center_x, self.target_center_y)
        offset.translate(self.x_pos_deg, self.y_val)

        self.current_target.setTransform(offset)
        self.scene.addItem(self.current_target)

        return target

    def setPosition(self, new_pos: QPointF):
        self.current_target.setTransform(QTransform.fromTranslate(
                                        self.participant_display.center_x - self.target_position.x() * self.operator_display.ppd,
                                        self.participant_display.center_y - self.target_position.y() * self.operator_display.ppd))

        self.viewport().update()
