
from PySide6.QtWidgets import QGraphicsScene, QGraphicsView
from PySide6.QtGui import QScreen, QTransform

from ocvl.fixation.targets import *


class ParticipantDisplay(QGraphicsView):

    def __init__(self, config: dict, parent=None):
        super(ParticipantDisplay, self).__init__(parent)

        self.part_config = config

        self.width = self.part_config.get("width_in_px", 800)
        self.height = self.part_config.get("height_in_px", 800)
        self.center = QPointF(self.part_config.get("center_x_px", self.width / 2),
                              self.part_config.get("center_y_px", self.height / 2))
        self.ppd = self.part_config.get("ppd", 20)

        self.target = TargetFactory.get_target(self.part_config.get("shape", TargetTypes.BULLSEYE),
                                               self.part_config.get("diameter", 1)*self.ppd,
                                               self.part_config.get("thickness", 0.1)*self.ppd,
                                               QColor(self.part_config.get("color", "orange")))
        # In degrees
        self.target_position = QPointF(0, 0)

        self.scene = QGraphicsScene(0, 0, self.width, self.height, self)

        self.setScene(self.scene)
        self.setMaximumSize(self.width, self.height)
        self.setMinimumSize(self.width, self.height)


        display_monitor = 0
        #send it to a different monitor and make full screen
        monitors = QScreen.virtualSiblings(self.screen())
        monitor = monitors[display_monitor].availableGeometry()
        self.move(monitor.left(), monitor.top())

        self.target.setTransform(QTransform.fromTranslate(self.center.x(), self.center.y()))
        self.scene.addItem(self.target)

        self.setFrameStyle(0)
        self.viewport().update()

    def setTarget(self, target: Target) -> Target:
        self.scene.clear()
        self.viewport().update()

        self.target = target

        self.target.setTransform(QTransform.fromTranslate(self.center.x() + self.target_position.x() * self.ppd,
                                                          self.center.y() - self.target_position.y() * self.ppd))

        self.scene.addItem(self.target)

        return target

    def setPosition(self, new_pos: QPointF):
        self.target_position = new_pos

        self.target.setTransform(QTransform.fromTranslate(self.center.x() + self.target_position.x() * self.ppd,
                                                          self.center.y() - self.target_position.y() * self.ppd))

        self.viewport().update()
