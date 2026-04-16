
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
        defaults = self.config.config.get("fixation_default").split("/")

        if defaults[0] == 'on':
            self.config.target_vis = True
        else:
            self.config.target_vis = False

        self.config.center_x_og = self.window().width() / 2
        self.config.center_y_og = self.window().height() / 2

        self.config.target_center_x = self.config.center_x_og
        self.config.target_center_y = self.config.center_y_og

        self.current_target = self.config.target_shape
        self.current_target.setTransform(QTransform.fromTranslate(self.config.target_center_x, self.config.target_center_y))
        self.scene.addItem(self.current_target)

        self.config.shapeChanged.connect(self.setTarget)
        self.config.xChanged.connect(self.updateTransform)
        self.config.yChanged.connect(self.updateTransform)

        self.setFrameStyle(0)
        self.viewport().update()

    def setTarget(self, target: Target):
        self.scene.clear()
        self.viewport().update()

        self.current_target = target

        offset = QTransform.fromTranslate(self.config.target_center_x, self.config.target_center_y)
        offset.translate(self.config.x_pos_deg, self.config.y_val)

        self.current_target.setTransform(offset)
        self.scene.addItem(self.current_target)

        return target

    def updateTransform(self):

        offset = QTransform.fromTranslate(self.config.target_center_x, self.config.target_center_y)
        offset.translate(self.config.x_pos_deg, self.config.y_val)

        self.current_target.setTransform(offset)
        self.viewport().update()
