
from PySide6.QtWidgets import QGraphicsScene, QGraphicsView
from PySide6.QtGui import QScreen, QTransform

from ocvl.fixation.targets import *

class NuclearTarget(QGraphicsView):

    # maybe want to put this in the config file
    # The number of ppd of the screen we'll be projecting to (e.g. Lightcrafter, Projector, etc).
    SCREEN_PPD = 20

    def __init__(self, var):
        super().__init__()

        self.scene = QGraphicsScene(0, 0, 800, 800, self)

        self.setScene(self.scene)
        self.setMaximumSize(800, 800)
        self.setMinimumSize(800, 800)

        self.var = var
        display_monitor = 0
        #send it to a different monitor and make full screen
        monitors = QScreen.virtualSiblings(self.screen())
        monitor = monitors[display_monitor].availableGeometry()
        self.move(monitor.left(), monitor.top())

        self.init = 1
        defaults = self.var.config.get( "fixation_default").split("/")

        if defaults[0] == 'on':
            self.var.target_vis = True
        else:
            self.var.target_vis = False

        self.var.center_x_og = self.window().width() / 2
        self.var.center_y_og = self.window().height() / 2

        self.var.target_center_x = self.var.center_x_og
        self.var.target_center_y = self.var.center_y_og

        self.current_target = self.var.target_shape
        self.current_target.setTransform(QTransform.fromTranslate(self.var.target_center_x, self.var.target_center_y))
        self.scene.addItem(self.current_target)

        self.var.shapeChanged.connect(self.setTarget)
        self.var.xChanged.connect(self.updateTransform)
        self.var.yChanged.connect(self.updateTransform)

        self.setFrameStyle(0)
        self.viewport().update()

    def setTarget(self, target: Target):
        self.scene.clear()
        self.viewport().update()

        self.current_target = target

        offset = QTransform.fromTranslate(self.var.target_center_x, self.var.target_center_y)
        offset.translate(self.var.x_pos, self.var.y_val)

        self.current_target.setTransform(offset)
        self.scene.addItem(self.current_target)

        return target

    def updateTransform(self):

        offset = QTransform.fromTranslate(self.var.target_center_x, self.var.target_center_y)
        offset.translate(self.var.x_pos, self.var.y_val)

        self.current_target.setTransform(offset)
        self.viewport().update()
